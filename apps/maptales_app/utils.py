from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import datetime
import os

def get_model_name(model):
    type = ContentType.objects.get_for_model(model)
    return type.app_label+"."+type.name.replace(" ", "_")
    
 