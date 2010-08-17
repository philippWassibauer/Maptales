from django import template
from django.contrib.contenttypes.models import ContentType
from maptales_app.utils import get_model_name

register = template.Library()


def object_to_content_type(object):
    try:
        return ContentType.objects.get_for_model(object).id
    except:
        return ""

register.filter(object_to_content_type)



def object_to_model_name(object):
    try:
        return get_model_name(object)
    except:
        return ""

register.filter(object_to_model_name)


