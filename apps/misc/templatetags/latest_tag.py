from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template import Library, Node, TemplateSyntaxError
from django.template import Variable, resolve_variable
from django.template import loader
from django.db.models import get_model
from django import template

register = Library()


@register.tag
def latest(parser, token):
    args = token.split_contents()
    if len(args) != 6:
        raise template.TemplateSyntaxError(
            "'%s' statement requires the form {% %s model field count as varname %}." % (
                args[0]))
    return LatestNode(args[1], args[2], args[3], args[5])



class LatestNode(template.Node):
    def __init__(self, class_type, field, count, var_name):
        self.class_type = class_type
        self.field = field
        self.count = count
        self.var_name = var_name

    def get_context(self, top_context):
        for context in top_context.dicts:
            if self.var_name in context:
                return context
        return top_context

    def render(self, context):
        model = get_model(*self.class_type.split('.'))
        content_type = ContentType.objects.get_for_model(model)
        try:
            objects = model.objects.all().order_by(self.field)[0:self.count]
            self.get_context(context)[self.var_name] = objects
        except template.VariableDoesNotExist:
            self.get_context(context)[self.var_name] = ''
        return ''
