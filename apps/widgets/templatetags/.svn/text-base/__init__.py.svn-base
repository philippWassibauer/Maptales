from django.template import Library
from django.conf import settings
from django.contrib.sites.models import Site

register = Library()

@register.inclusion_tag("addthis/addthis.html")
def add_this(url, source=""):
    current_site = Site.objects.get(id=settings.SITE_ID)
    addthis_url = "http://"+str(current_site)+url
    return {"addthis_url": addthis_url,
            "source": source}
