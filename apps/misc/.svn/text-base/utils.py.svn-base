from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

_inbox_count_sources = None

def inbox_count_sources():
    global _inbox_count_sources
    if _inbox_count_sources is None:
        sources = []
        for path in settings.COMBINED_INBOX_COUNT_SOURCES:
            i = path.rfind('.')
            module, attr = path[:i], path[i+1:]
            try:
                mod = __import__(module, {}, {}, [attr])
            except ImportError, e:
                raise ImproperlyConfigured('Error importing request processor module %s: "%s"' % (module, e))
            try:
                func = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a "%s" callable request processor' % (module, attr))
            sources.append(func)
        _inbox_count_sources = tuple(sources)
    return _inbox_count_sources


def get_send_mail():
    """
    A function to return a send_mail function suitable for use in the app. It
    deals with incompatibilities between signatures.
    """
    # favour django-mailer but fall back to django.core.mail
    if "mailer" in settings.INSTALLED_APPS:
        from mailer import send_mail
    else:
        from django.core.mail import send_mail as _send_mail
        def send_mail(*args, **kwargs):
            del kwargs["priority"]
            return _send_mail(*args, **kwargs)
    return send_mail

def make_unique(object_with_slug, func_is_unique):
    """
    A function to return a unique slug
    func_is_unique must be a function that tests if the new slug is unique
    """
    if not callable(func_is_unique):
        raise TypeError("func_is_unique must be callable")
    
    slug = object_with_slug.slug
    while not func_is_unique(object_with_slug):
        slug = slug + '_'
        object_with_slug.slug = slug
    return slug

def safetylevel_filter(query, creator_field, user):
    try:
        if not user.is_authenticated():
            return query.filter(Q(safetylevel__lte=1)|Q(**{creator_field+"__id": user.id}))
        if user.is_staff:
            return query
        elif user.is_smith:
            return query.filter(Q(safetylevel__lte=2)|Q(**{creator_field+"__id": user.id}))
        else:
            return query.filter(Q(safetylevel__lte=1)|Q(**{creator_field+"__id": user.id}))
    except:
        return query.filter(Q(safetylevel__lte=1)|Q(**{creator_field+"__id": user.id}))


def get_target_object(uuid):
    content_type = get_target_contenttype(uuid)
    content_type_split = uuid.split(".")
    target_object = content_type.get_object_for_this_type (pk=content_type_split[2])
    return target_object

def get_target_contenttype(uuid):
    content_type_split = uuid.split(".")
    content_type = ContentType.objects.get(app_label=content_type_split[0],
                                           name=content_type_split[1])
    return content_type
