from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
 
class ProfileAppHook(CMSApp):
    name = _("Profile App")
    urls = ["profiles.urls"]
 
apphook_pool.register(ProfileAppHook)