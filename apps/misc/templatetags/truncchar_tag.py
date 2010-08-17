from django import template
register = template.Library()

@register.filter
def truncchar(value, arg):
    if not isinstance(value, str):
       value = unicode(value)

    if len(value) < arg:
        return value
    else:
        return value[:arg] + '...'
