from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
 
class AvatarAppHook(CMSApp):
    name = _("Avatar App")
    urls = ["avatar.urls"]
 
apphook_pool.register(AvatarAppHook)