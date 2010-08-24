from django.db.models import signals
from activity_stream.models import ActivityTypes 
from django.utils.translation import ugettext_noop as _
import sys

try:
    from maptales_app import models as maptales_app

    def create_notice_types(app, created_models, verbosity, **kwargs):
        ActivityTypes.objects.get_or_create(name="posted_comment", is_batchable=False)
        ActivityTypes.objects.get_or_create(name="badge_awarded", is_batchable=False)
        
    signals.post_syncdb.connect(create_notice_types, sender=maptales_app)
except ImportError:
    print >> sys.stderr, "Skipping creation of NoticeTypes as notification app not found"