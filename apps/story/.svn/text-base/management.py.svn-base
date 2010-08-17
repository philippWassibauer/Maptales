from django.db.models import signals

from django.utils.translation import ugettext_noop as _
import activity_stream.models
from activity_stream.models import ActivityTypes
import sys

try:
    def create_activity_types(app, created_models, verbosity, **kwargs):
        ActivityTypes.objects.get_or_create(name="edited_story", batch_time_minutes=30, is_batchable=True)
        ActivityTypes.objects.get_or_create(name="created_story", is_batchable=False)
    signals.post_syncdb.connect(create_activity_types, sender=activity_stream.models)
except ImportError:
    print >> sys.stderr, "Skipping creation of ActivityTypes as  app not found"
