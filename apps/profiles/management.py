from django.db.models import signals

from django.utils.translation import ugettext_noop as _
import sys
from activity_stream.models import ActivityTypes
import activity_stream.models

try:
    from notification import models as notification

    def create_activity_types(app, created_models, verbosity, **kwargs):
        ActivityTypes.objects.get_or_create(name="edited_profile", batch_time_minutes=30, is_batchable=True)
        ActivityTypes.objects.get_or_create(name="user_location_update", batch_time_minutes=30, is_batchable=True)

    signals.post_syncdb.connect(create_activity_types, sender=activity_stream.models)
    
except ImportError:
    print >> sys.stderr, "Skipping creation of NoticeTypes as notification app not found"
