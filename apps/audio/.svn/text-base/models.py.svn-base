from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from photologue.models import *
from django.utils.translation import ugettext_lazy as _
from maptales_app.models import PRIVACY_LEVELS


class AudioImage(ImageModel):
    audio_item = models.OneToOneField('Audio', primary_key=True)


class AudioField(models.FileField):
    def __init__(self, verbose_name=None, name=None, title_field=None, duration_field=None, bitrate_field=None, **kwargs):
        self.title_field, self.duration_field, self.bitrate_field = title_field, duration_field, bitrate_field
        models.FileField.__init__(self, verbose_name, name, **kwargs)

    def get_internal_type(self):
        return "FileField"

    def contribute_to_class(self, cls, name):
        super(AudioField, self).contribute_to_class(cls, name)
        if not self.title_field:
            setattr(cls, 'get_%s_title' % self.name, curry(_get_title, field=self))
        if not self.duration_field:
            setattr(cls, 'get_%s_duration' % self.name, curry(_get_duration, field=self))
        if not self.bitrate_field:
            setattr(cls, 'get_%s_bitrate' % self.name, curry(_get_bitrate, field=self))

def _get_audio_details(obj, field):
    cachename = "__%s_audio_details" % field.name
    if not hasattr(self, cachename):
        import mutagen
        filename = obj._get_FIELD_filename(field)
        file = mutagen.File(filename)
        details = {
            'duration': datetime.timedelta(seconds=file.info.length),
            'bitrate': file.info.bitrate,
        }
        try:
            details['title'] = unicode(file['title'])
        except KeyError:
            details['title'] = unicode(file['TIT2'])
        setattr(obj, cachename, details)
    return getattr(self, cachename)

def _get_title(obj, field):
    return _get_audio_details(obj, field)['title']

def _get_duration(obj, field):
    return _get_audio_details(obj, field)['duration']

def _get_bitrate(obj, field):
    return _get_audio_details(obj, field)['bitrate']


    
# Create your models here.
class Audio(models.Model):
    title           = models.CharField(max_length=300, blank=True)
    creator         = models.ForeignKey(User, related_name="added_audios")
    comment         = models.CharField( max_length=250, blank=True )
    audio_file      = AudioField(upload_to='audio_files')
    cover           = models.ImageField("Cover (image file)", upload_to='audio_cover', blank=True)

    last_modified   = models.DateTimeField(auto_now=True, editable=False)
    date_added      = models.DateTimeField(auto_now_add=True, editable=False)

    safetylevel = models.IntegerField(_('safetylevel'), choices=PRIVACY_LEVELS, default=1,  help_text=_('Who can listen?'))

    def save(self, force_insert=False, force_update=False):
        super(self.__class__, self).save(force_insert, force_update) # Call the "real" save() method.
        if self.cover:
            self.audioimage = AudioImage()
            self.audioimage.image = self.cover
            self.audioimage.audio_item = self
            self.audioimage.save()

    def rendered(self):
        return mark_safe(render_to_string('audioplayer.html', { 'audios': [ self ] }))
        
    class Meta:
        ordering = [ '-last_modified' ]

        

