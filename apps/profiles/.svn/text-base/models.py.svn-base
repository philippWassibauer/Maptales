from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from timezones.fields import TimeZoneField

class Country(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = [ 'name' ]


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))

    first_name = models.CharField(_('firstname'), max_length=200, blank=True)
    last_name = models.CharField(_('lastname'), max_length=200, blank=True)

    country = models.ForeignKey(Country, null=True, blank=True)
    city = models.CharField(_('city'), max_length=200, blank=True)
    job = models.CharField(_('job'), max_length=200, blank=True)
    enterprise = models.CharField(_('enterprise'), max_length=200, blank=True)
    
    website = models.URLField(_('website'), null=True, blank=True, verify_exists=False)
    skype = models.CharField(_('skype'), max_length=200, blank=True)

    about = models.TextField(_('statement'), null=True, blank=True)

    location = models.PointField(srid=4326, blank=True, null=True)
    path = models.LineStringField(srid=4326, blank=True, null=True)
    
    public_profile = models.BooleanField(_('public profile'), default=True)
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        if self.first_name:
            return self.first_name
        else:
            return self.user.username
    
    def is_filled_out(self):
        avatar = Avatar.objects.get(user=self.user)
        if self.first_name and self.last_name and self.about and avatar:
            return True
        else:
            return False
        
    def get_absolute_url(self):
        return ('profile_detail', None, {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)

    def get_num_of_location_updates(self):
        if self.path:
            return len(self.path)-1 # -1 because first point is double since a line cannot have just one point
        else:
            return 0
            
    def render_inline(self):
        return mark_safe(render_to_string('profiles/render_inline.html', { 'profile': self }))

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)