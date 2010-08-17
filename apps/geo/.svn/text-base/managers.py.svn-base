from django.db import models
from geo.models import *

class ModelTaggedItemManager(models.Manager):
    """
    A manager for retrieving model instances based on their geoinformation.
    """
    def related_to(self, obj, queryset=None, num=None):
        if queryset is None:
            return GeoPointTag.objects.get_related(obj, self.model, num=num)
        else:
            return GeoPointTag.objects.get_related(obj, queryset, num=num)

    def with_all(self, tags, queryset=None):
        if queryset is None:
            return GeoPointTag.objects.get_by_model(self.model, tags)
        else:
            return GeoPointTag.objects.get_by_model(queryset, tags)

    def with_any(self, tags, queryset=None):
        if queryset is None:
            return GeoPointTag.objects.get_union_by_model(self.model, tags)
        else:
            return GeoPointTag.objects.get_union_by_model(queryset, tags)
