from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.db.models.signals import post_init
from django.conf import settings
from tagging.fields import TagField
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from datetime import datetime
from maptales_app.models import PRIVACY_LEVELS
from maptales_app.utils import get_model_name
from django.template import Context, Template
from photologue.models import ImageModel

class VimeoToken(models.Model):
    name            = models.CharField(max_length=300)
    token           = models.CharField(max_length=300)
    def __unicode__(self):
        return self.name+" "+self.token

class VideoImage(ImageModel):
    video = models.OneToOneField('Video', primary_key=True, related_name="videoimage")
    
class Video(models.Model):
    title           = models.CharField(_('title'), max_length=300, blank=True)
    comment         = models.TextField(_('comment'), max_length=250, blank=True )
    creator         = models.ForeignKey(User, related_name="added_videos")
    was_uploaded    = models.BooleanField(blank=True)
    
    from_html_code  = models.BooleanField(blank=True, default=False)
    html_code       = models.TextField(_('html code'), max_length=850, blank=True )
    
    is_viewable     = models.BooleanField(default=True)
    import_url      = models.CharField(max_length=300, blank=True)
    thumbnail_url   = models.CharField(max_length=300, blank=True)
    
    external_id     = models.CharField(max_length=300, blank=True)
    original_file   = models.FileField (upload_to='videoupload', blank=True)
    tags            = TagField()
    ticket_id       = models.CharField(max_length=300, blank=True)
    safetylevel = models.IntegerField(_('safetylevel'), choices=PRIVACY_LEVELS, default=1,  help_text=_('Who can see this Video?'))
        
    last_modified   = models.DateTimeField(auto_now=True, editable=False)
    date_added      = models.DateTimeField(auto_now_add=True, editable=False, default=datetime.now())
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('show_video', None, {
            'id': self.id,
        })
    get_absolute_url = models.permalink(get_absolute_url)

    def rendered(self):
        return mark_safe(render_to_string('video_teaser.html', { 'video': self }))
        
    class Meta:
        ordering = [ '-last_modified' ]
      
    def get_geojson(self):
        c = Context({"type": get_model_name(self),
                "self": self})

        t = Template("""{"type": "{{type}}",\
                "id": "{{self.id}}",\
                "title": "{{self.title}}",\
                "body": "{{self.body}}",\
                "publish": "{{self.publish|date}} ",\
                "slug": "{{self.slug}}",\
                "marker_image": "{{self.videoimage.get_50x50_url}}",\
                {% if self.has_location %}\
                    "location": {% autoescape off %}{{self.location.geojson}}{% endautoescape %},\
                {% endif %}\
                "location_name": "{{self.location_name}}" }""")
        return t.render(c)
    
    def save(self, *args, **kwargs):
        super(Video, self).save(*args, **kwargs)
        if not VideoImage.objects.filter(video=self).all():
            import urllib
            import os
            from django.core.files.base import ContentFile
            story_image = VideoImage(video=self)
            story_image.image.save(os.path.basename("video_thumb_"+str(self.id)),
                                   ContentFile(urllib.urlopen(self.thumbnail_url).read()))
            story_image.save()

import geo
geo.register(Video)

def check_vimeo_status(sender, instance, **kwargs):
    from video.rest.vimeoPy import VimeoClient
    if not instance.is_viewable:
        vimeoClient = VimeoClient(settings.VIMEO_API_KEY, settings.VIMEO_API_SECRET)
        rsp = vimeoClient.call("vimeo.videos.checkUploadStatus", {"ticket_id": instance.ticket_id} )
        if(rsp.attributes['stat'].value=="ok"):
            data = rsp.getElementsByTagName("ticket")[0]
            if data.attributes['is_uploading'].nodeValue=="0":
                if data.attributes['is_uploading'].nodeValue=="0":
                    rsp = vimeoClient.call("vimeo.videos.getThumbnailUrl", {"video_id": instance.external_id, "size":"160x120"} )
                    thumbnail_url = rsp.getElementsByTagName("thumbnail")[0].childNodes[0].nodeValue
                    instance.thumbnail_url = thumbnail_url
                    instance.is_viewable = True
                    instance.save()

post_init.connect(check_vimeo_status, sender=Video)


class VideoPool(models.Model):
    """
    model for a photo to be applied to an object
    """

    video           = models.ForeignKey(Video)
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    content_object  = generic.GenericForeignKey()
    created_at      = models.DateTimeField(_('created_at'), default=datetime.now)

    class Meta:
        # Enforce unique associations per object
        unique_together = (('video', 'content_type', 'object_id'),)
        verbose_name = _('videopool')
        verbose_name_plural = _('videopools')

