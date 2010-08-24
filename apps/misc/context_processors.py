from django.conf import settings as _settings
from django.contrib.sites.models import Site
from misc.utils import inbox_count_sources

def contact_email(request):
    return {'contact_email': getattr(_settings, 'CONTACT_EMAIL', '')}

def site_name(request):
    return {'site_name': getattr(_settings, 'SITE_NAME', '')}
    
def domain_name(request):
    return {'domain': Site.objects.get_current() }

def combined_inbox_count(request):
    """
    A context processor that uses other context processors defined in
    setting.COMBINED_INBOX_COUNT_SOURCES to return the combined number from
    arbitrary counter sources.
    """
    count = 0
    for func in inbox_count_sources():
        counts = func(request)
        if counts:
            for value in counts.itervalues():
                try:
                    count = count + int(value)
                except (TypeError, ValueError):
                    pass
    return {'combined_inbox_count': count,}



def settings(request):
    return {'settings': _settings}
