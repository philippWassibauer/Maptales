from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
 
class MaptalesAppHook(CMSApp):
    name = _("Maptales App")
    urls = ["maptales_app.urls"]
 
apphook_pool.register(MaptalesAppHook)