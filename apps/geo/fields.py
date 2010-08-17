"""
A custom Model Field for tagging.
"""
from django.db.models import signals
from django.db.models.fields import CharField
from django.utils.translation import ugettext_lazy as _
from geo.models import GeoAbstractModel
from django.contrib.contenttypes.models import ContentType

class LocationField(object):
    """
    retreives the location and caches the relation locally...in case it is used
    more often
    """
    
    def __get__(self, instance, owner=None):
        if instance is None:
            return None

        location = self._get_instance_location_cache(instance)
        if location is None:
            if instance.pk is None:
                self._set_instance_location_cache(instance, '')
            else:
                ct = ContentType.objects.get_for_model(instance)
                geo_taggs = GeoAbstractModel.objects.filter(content_type=ct,
                                                   object_id=instance.pk)
                if geo_taggs:
                    location = geo_taggs[0].downcast().location
                    return location
                else:
                    return None
                self._set_instance_location_cache(
                    instance, location)
        return self._get_instance_location_cache(instance)

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError(_('%s can only be set on instances.') % self.name)
        self._set_instance_location_cache(instance, value)
    
    def _get_instance_location_cache(self, instance):
        return getattr(instance, '_location_cache', None)

    def _set_instance_location_cache(self, instance, location):
        setattr(instance, '_location_cache', location)
