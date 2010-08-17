from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
 
class StoryAppHook(CMSApp):
    name = _("Story App")
    urls = ["story.urls"]
 
apphook_pool.register(StoryAppHook)