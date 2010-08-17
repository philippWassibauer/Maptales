from django.db.models import signals

from django.utils.translation import ugettext_noop as _
import sys
from activity_stream.models import ActivityTypes
import geo.models

def create_activity_types(app, created_models, verbosity, **kwargs):
    try:
        ActivityTypes.objects.get_or_create(name="placed", batch_time_minutes=30, is_batchable=True)
        ActivityTypes.objects.get_or_create(name="geodata_uploaded", is_batchable=False)
    except:
        pass
signals.post_syncdb.connect(create_activity_types, sender=geo.models)
