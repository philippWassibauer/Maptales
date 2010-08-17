"""
tagcon: a template tag constructor library for Django

Based on the syntax and implementation of Django's Model and Form classes.
"""
from __future__ import absolute_import

import datetime
import re
import sys
import weakref

from django import template
from django.conf import settings
from django.db import models
from django.utils.encoding import force_unicode


__all__ = (
    'Arg',
    'DateTimeArg',
    'IntegerArg',
    'ModelInstanceArg',
    'StringArg',
    'TemplateTag',
    'TemplateTagArgumentMissing',
    'TemplateTagValidationError',
)


class TemplateTagValidationError(template.TemplateSyntaxError):
    pass


class TemplateTagArgumentMissing(KeyError):
    pass
    # # exceptions use __str__, not __unicode__ or __repr__
    # def __str__(self):
    #     return self.args[0]


class Arguments(dict):
    def __getattr__(self, name):
        if name.endswith('_'):
            name = name.rstrip('_')
        return self[name]

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            err_msg = "'%s' (Did you forget" \
            " to call '.resolve(context)'?)" % (key,)
            raise TemplateTagArgumentMissing(err_msg)


_split_single = r"""
    ([^\s",]*"(?:[^"\\]*(?:\\.[^"\\]*)*)"[^\s,]*|
     [^\s',]*'(?:[^'\\]*(?:\\.[^'\\]*)*)'[^\s,]*|
     [^\s,]+)
"""
_split_multi = r"""%s(?:\s*,\s*%s)*""" % (_split_single, _split_single)
_split_single_re = re.compile(_split_single, re.VERBOSE)
_split_multi_re = re.compile(_split_multi, re.VERBOSE)

def _smarter_split(input):
    input = force_unicode(input)
    for multi_match in _split_multi_re.finditer(input):
        hit = []
        for single_match in _split_single_re.finditer(multi_match.group(0)):
            hit.append(single_match.group(0))
        if len(hit) == 1:
            yield hit[0]
        else:
            yield hit


CLASS_NAME_RE = re.compile(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))')
def _get_tag_name(class_name):
    name = CLASS_NAME_RE.sub(r'_\1', class_name).lower().strip('_')
    if name.endswith('_tag'):
        name = name[:-4]
    return name


def _cardinal(n):
    """
    Return the cardinal number for an integer.

    Returns words (e.g., "one") for 0 through 10; returns digits for numbers
    greater than 10.

    TODO: check usage guide to decide if 9 or 10 should be the cutoff.
    """
    n = int(n)
    if n < 0:
        raise ValueError("Argument must be >= 0")
    try:
        return (u'zero', u'one', u'two', u'three', u'four', u'five',
                u'six', u'seven', u'eight', u'nine', u'ten')[n]
    except IndexError:
        return unicode(n)


def _ordinal(n):
    """
    Return the ordinal number for an integer.

    Differs from the humanize version as it returns full words (e.g., "first")
    for 1 through 9, and does not work for numbers less than 1.
    """
    n = int(n)
    if n < 1:
        raise ValueError("Argument must be >= 1")
    try:
        return (u'first', u'second', u'third', u'fourth', u'fifth', u'sixth',
                u'seventh', u'eighth', u'ninth')[n-1]
    except IndexError:
        t = ('th', 'st', 'nd', 'rd') + (('th',) * 6)
        if n % 100 in (11, 12, 13):
            return u"%d%s" % (n, t[0])
        return u'%d%s' % (n, t[n % 10])


def _pluralize(singular, quantity, suffix='s'):
    if quantity == 1:
        return singular
    return '%s%s' % (singular, suffix)


def _verbose_quantity(singular, quantity, suffix='s'):
    try:
        quantity = int(quantity)
    except TypeError:
        try:
            quantity = len(quantity)
        except TypeError:
            raise TypeError("Quantity must be an integer or sequence.")
    return '%s %s' % (
        _cardinal(quantity),
        _pluralize(singular, quantity, suffix=suffix),
    )


def _unroll_render(s):
    if s is None:
        err_msg = "'render' must return a string or an iterable (got None)"
        raise TypeError(err_msg)
    if isinstance(s, basestring):
        return s
    return ''.join(unicode(piece) for piece in s)


def _invalid_template_string(var):
    if settings.TEMPLATE_STRING_IF_INVALID:
        if template.invalid_var_format_string is None:
            template.invalid_var_format_string = \
                '%s' in settings.TEMPLATE_STRING_IF_INVALID
        if template.invalid_var_format_string:
            return settings.TEMPLATE_STRING_IF_INVALID % var
    return settings.TEMPLATE_STRING_IF_INVALID


def _wrap_render(unwrapped_render):
    def render(self, context):
        try:
            return _unroll_render(unwrapped_render(self, context))
        except template.VariableDoesNotExist, exc:
            if self.silence_errors:
                return _invalid_template_string(exc.var)
            raise
        except Exception, exc:
            if self.silence_errors:
                return ''
            raise
    return render


class TemplateTagBase(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(TemplateTagBase, cls).__new__
        parents = [b for b in bases if isinstance(b, TemplateTagBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)
        # module = attrs.pop('__module__')
        try:
            meta = attrs.pop('Meta')
        except KeyError:
            meta = None
        try:
            library = meta.library
        except AttributeError:
            # try auto-lookup
            module = sys.modules[attrs['__module__']]
            library = getattr(module, 'register', None)
        if not isinstance(library, template.Library):
            raise TypeError("A valid library is required.")

        # use supplied name, or generate one from class name
        tag_name = getattr(meta, 'name', _get_tag_name(name))
        attrs['name'] = tag_name

        attrs['silence_errors'] = getattr(meta, 'silence_errors', False)

        # wrap render so it can optionally yield strings as a generator, and so
        # we can catch exceptions if necessary
        unwrapped_render = attrs.pop('render')
        attrs['render'] = _wrap_render(unwrapped_render)

        # positional tag arguments
        positional_args = attrs.pop('_', ())
        # shortcut for single-arg case
        if isinstance(positional_args, Arg):
            positional_args = (positional_args,)
        else:
            for arg in positional_args:
                if isinstance(arg, Arg):
                    if not arg.name:
                        raise TypeError(
                            "Positional arguments must have 'name' specified."
                        )
                    # positional args are always required
                    arg.required = True
                elif not isinstance(arg, basestring):
                    raise TypeError(
                        "positional args must be Arg instances or strings"
                    )
                elif not arg:
                    raise ValueError("Empty strings are not valid arguments.")
        attrs['_positional_args'] = positional_args
        all_args = dict(
            (arg.name, arg) for arg in positional_args if isinstance(arg, Arg)
        )

        # keyword tag arguments
        keyword_args = {}
        # can't use iteritems, since we mutate attrs
        keys = attrs.keys()
        for key in keys:
            value = attrs[key]
            if not isinstance(value, Arg):
                continue
            del attrs[key]
            if key.endswith('_'):
                # hack for reserved names, e.g., "for_" -> "for"; the tag's
                # .args object understands this, too
                key = key.rstrip('_')
            value.keyword = key
            if not value.name:
                value.name = key
            keyword_args[key] = value
            all_args[value.name] = value
        # _keyword_args is keyed by *keyword*
        attrs['_keyword_args'] = keyword_args
        # _args and _positional_args are keyed by *arg/var name*
        attrs['_args'] = all_args

        # create the new class
        new_class = super_new(cls, name, bases, attrs)

        # register the tag
        library.tag(tag_name, new_class)

        return new_class


class TemplateTag(template.Node):
    """
    A template tag.
    """
    __metaclass__ = TemplateTagBase

    def __init__(self, parser, token):
        # don't keep the parser alive
        self.parser = weakref.proxy(parser)
        self.args = Arguments()
        self._vars = {}
        self._raw_args = list(_smarter_split(token.contents))[1:]
        # self._raw_args = token.split_contents()[1:]
        self._process_positional_args()
        self._process_keyword_args()

    def _process_positional_args(self):
        for i, arg in enumerate(self._positional_args):
            pos = i + 1
            if isinstance(arg, basestring):
                name = arg
            else:
                name = arg.name
            try:
                raw_arg = self._raw_args.pop(0)
            except IndexError:
                err_msg = "'%s' takes at least %s" % (
                    self.name,
                    _verbose_quantity('argument', self._positional_args),
                )
                raise template.TemplateSyntaxError(err_msg)
            if isinstance(arg, basestring):
                if raw_arg != arg:
                    err_msg = "%s argument to '%s' must be '%s'" % (
                        _ordinal(pos).capitalize(), self.name, name,
                    )
                    raise template.TemplateSyntaxError(err_msg)
            else:
                self._set_var(arg, raw_arg)

    def _process_keyword_args(self):
        while self._raw_args:
            keyword = self._raw_args.pop(0)
            try:
                arg = self._keyword_args[keyword]
            except KeyError:
                err_msg = "'%s' does not take argument '%s'" % (
                    self.name, keyword,
                )
                raise template.TemplateSyntaxError(err_msg)
            if arg.flag:
                self._set_var(arg, True)
                continue
            try:
                value = self._raw_args.pop(0)
            except IndexError:
                err_msg = "'%s' argument to '%s' missing value" % (
                    keyword,
                    self.name,
                )
                raise template.TemplateSyntaxError(err_msg)
            self._set_var(arg, value)
        # handle missing items: required, default, flag
        for keyword, arg in self._keyword_args.iteritems():
            if arg.name in self._vars:
                continue
            if arg.flag:
                self._set_var(arg, False)
                continue
            if arg.required:
                err_msg = "'%s' argument to '%s' is required" % (
                    keyword, self.name,
                )
                raise template.TemplateSyntaxError(err_msg)
            self._set_var(arg, arg.default)

    def _compile_filter(self, arg, value):
        fe = template.FilterExpression(value, self.parser)
        if not arg.resolve and fe.var.lookups:
            fe.var.lookups = None
            fe.var.literal = fe.var.var
        return fe

    def _set_var(self, arg, value):
        if value and isinstance(value, (list, tuple)):
            self._vars[arg.name] = [
                self._compile_filter(arg, v) for v in value
            ]
            return
        if not isinstance(value, basestring):
            # non-string default value; short-circuit as FilterExpression can
            # only handle strings
            self._vars[arg.name] = value
            return
        self._vars[arg.name] = self._compile_filter(arg, value)

    def clean(self):
        """
        Additional tag-wide argument cleaning after each individual Arg's
        ``clean`` has been called.
        """
        return

    def render(self, context):
        raise NotImplementedError(
            "TemplateTag subclasses must implement this method."
        )

    def _resolve_single(self, context, value):
        if isinstance(value, template.FilterExpression):
            if isinstance(value.var, template.Variable):
                # we *want* VariableDoesNotExist to get raised, but
                # FilterExpression normally swallows it, so we first resolve
                # the encapsulated Variable directly
                try:
                    value.var.resolve(context)
                except VariableDoesNotExist, exc:
                    exc.var = value.var.var
                    raise
            # resolve the FilterExpression as normal
            value = value.resolve(context)
        elif isinstance(value, template.Variable):
            value = value.resolve(context)
        return value

    def resolve(self, context):
        """
        Resolve variables and run clean methods.

        Cleaning happens after variable/filter resolution.

        Cleaning order is similar to forms:

        1) The argument's ``.clean()`` method.
        2) The tag's ``clean_ARGNAME()`` method, if any.
        3) The tag's ``.clean()`` method.
        """
        for k, v in self._vars.iteritems():
            if isinstance(v, (list, tuple)):
                v = [self._resolve_single(context, x) for x in v]
            else:
                v = self._resolve_single(context, v)
            arg = self._args[k]
            v = arg.base_clean(v)
            try:
                tag_arg_clean = getattr(self, 'clean_%s' % (arg.name,))
            except AttributeError:
                pass
            else:
                v = tag_arg_clean(v)
            self.args[k] = v
        self.clean()


class Arg(object):
    """
    A template tag argument.

    ``name`` is the variable name, and is required if the argument is
    positional; otherwise it will use the keyword name by default.  This is
    *not* the keyword name (i.e., the name used in the tag iself).

    ``required`` and ``default`` are mutually exclusive, and only apply to
    keyword arguments; a positional argument is implicitly required.

    ``null`` determines whether a value of ``None`` can bypass validation via
    the argument's ``clean`` method; if ``null`` is false, a ``None`` value
    will simply be passed to ``clean`` normally.  (This will only apply if
    ``required`` is false and ``default`` is None.)

    ``resolve`` determines whether a non-literal string (i.e., not surrounded
    in quotes) will be resolved as a variable; if false, it will be interpreted
    as a string.

    ``multi`` determines if the argument's value may consist of multiple
    comma-separated items (which would each be resolved, or not, according to
    the value of ``resolve``).

    ``flag`` denotes a keyword argument that does *not* have a separate value;
    its value is true if they keyword is given, and false otherwise.

    TODO: raise an error on various invalid option combinations (e.g.,
    ``required`` and ``default``)
    """
    def __init__(self, name=None, required=False, default=None, null=False,
                 resolve=True, multi=False, flag=False):
        self.name = name
        self.required = required
        self.default = default
        self.null = null
        self.resolve = resolve
        self.multi = multi
        self.keyword = None
        self.flag = flag

    def base_clean(self, value):
        """
        Validation that always takes place.

        Don't override me; override ``clean`` instead.
        """
        if not self.multi and isinstance(value, (list, tuple)):
            err_msg = "Value for '%s' must be a single item." % (self.name,)
            raise TemplateTagValidationError(err_msg)
        if value is not None or not self.null:
            value = self.clean(value)
        return value

    def clean(self, value):
        """
        Validate the argument value.

        Subclasses should perform any munging here, raising
        ``TemplateTagValidationError`` as necessary.

        Filters are applied *before* ``clean`` is called.

        Note: if ``self.null`` is true, this will never get called.
        """
        return value


class IntegerArg(Arg):
    def clean(self, value):
        try:
            value = int(value)
        except (TypeError, ValueError), exc:
            raise TemplateTagValidationError(
                "Value for '%s' must be an integer (got %r)" % (
                    self.name,
                    value
                )
            )
        return value


class StringArg(Arg):
    def clean(self, value):
        if not isinstance(value, basestring):
            raise TemplateTagValidationError(
                "Value for '%s' must be a string" % (
                    self.name,
                )
            )
        return value


class DateTimeArg(Arg):
    def clean(self, value):
        if not isinstance(value, datetime.datetime):
            raise TemplateTagValidationError(
                "Value for '%s' must be a datetime instance" % (
                    self.name,
                )
            )
        return value


class ModelInstanceArg(Arg):
    def __init__(self, *args, **kwargs):
        try:
            model = kwargs.pop('model')
        except KeyError:
            err_msg = "A 'model' keyword argument is required"
            raise TypeError(err_msg)
        if not issubclass(model, models.Model):
            err_msg = "'model' must be a Model subclass"
            raise TypeError(err_msg)
        self.model_class = model
        super(ModelInstanceArg, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not isinstance(value, self.model_class):
            raise TemplateTagValidationError(
                "Value for '%s' must be an instance of %s.%s" % (
                    self.name,
                    self.model_class.__module__,
                    self.model_class.__name__,
                )
            )
        return value
