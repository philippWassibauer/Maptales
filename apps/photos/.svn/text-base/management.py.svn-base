from django.db.models import signals

from django.utils.translation import ugettext_noop as _
import photos.models
from activity_stream.models import ActivityTypes
import sys


def create_activity_types(app, created_models, verbosity, **kwargs):
    try:
        ActivityTypes.objects.get_or_create(name="uploaded_pictures", batch_time_minutes=30, is_batchable=True)
    except:
        pass

signals.post_syncdb.connect(create_activity_types, sender=photos.models)
