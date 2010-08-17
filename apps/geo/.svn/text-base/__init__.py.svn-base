from geo.fields import LocationField
from django.contrib.contenttypes.models import ContentType
from geo.models import GeoAbstractModel
from django.db.models import signals

registry = []

def has_location(self):
    return self.location \
           and (str(self.location.x) != str(float('NaN')) \
           and str(self.location.y) != str(float('NaN')))


def delete_signal(**kwargs):
    ct = ContentType.objects.get_for_model(kwargs['instance'])
    geo_taggs = GeoAbstractModel.objects.filter(content_type=ct,
                                       object_id=kwargs['instance'].pk)
    geo_taggs.delete()

def register(model, tag_descriptor_attr='location',
             tagged_item_manager_attr='geotagged'):
    
    if model in registry:
        raise AlreadyRegistered(
            _('The model %s has already been registered.') % model.__name__)
    registry.append(model)

    # Add tag descriptor
    setattr(model, tag_descriptor_attr, LocationField())
    setattr(model, "has_location", has_location)
    
    signals.pre_delete.connect(delete_signal, model, True)
    