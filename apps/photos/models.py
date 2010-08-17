#from django.db import models
from django.contrib.auth.models import User
from photologue.models import *
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from tagging.fields import TagField
import tagging

from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db import models
from maptales_app.utils import get_model_name

from django.template import Context, Template
from maptales_app.models import PRIVACY_LEVELS
import logging
from PIL import Image as PILImage
from geo.models import GeoAbstractModel
from geo.fields import LocationField
import geo

PUBLISH_CHOICES = (
    (1, _('Public')),
    (2, _('Private')),
)

IMAGE_EXIF_ORIENTATION_MAP = {
    1: 0,
    8: 90,
    3: 180,
    6: 270,
}

class PhotoSet(models.Model):
    """
    A set of photos
    """
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'))
    publish_type = models.IntegerField(_('publish_type'), choices=PUBLISH_CHOICES, default=1)
    tags = TagField()

    class Meta:
        verbose_name = _('photo set')
        verbose_name_plural = _('photo sets')


class Image(ImageModel):
    """
    A photo with its details
    """
    
    title = models.CharField(_('title'), max_length=200)
    title_slug = models.SlugField(_('slug'))
    caption = models.TextField(_('caption'), blank=True)
    date_added = models.DateTimeField(_('date added'), default=datetime.now, editable=False)
    is_public = models.BooleanField(_('is public'), default=True, help_text=_('Public photographs will be displayed in the default views.'))
    member = models.ForeignKey(User, related_name="added_photos", blank=True, null=True)
    safetylevel = models.IntegerField(_('safetylevel'), choices=PRIVACY_LEVELS, default=1,  help_text=_('privacy helptext'))
    photoset = models.ManyToManyField(PhotoSet, verbose_name=_('photo set'))
    tags = TagField()
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ("photo_details", [self.pk])
    
    def rotate_to_exif(self):
        try:
            exif_orientation = self.EXIF.get('Image Orientation', 1).values[0]
            orientation = IMAGE_EXIF_ORIENTATION_MAP[exif_orientation]
        except:
            orientation = 0
        self.rotate(orientation)
        
    def rotate(self, orientation):
        if(orientation>0 or orientation<0):
            image = PILImage.open(self.image.file)
            image = image.rotate(orientation)
            import os
            namesplit = self.image.file.name.split("/")
            filename = namesplit[-1]
            extension = filename.split(".")[-1]
            filename = filename.split(".")[0]
            
            newfile = ("/").join(namesplit[0:-1])+"/%s.%s"%(filename,extension)
            os.remove(self.image.file.name)
            image.save(newfile)
            self.image.save("%s.%s"%(filename,extension), ContentFile(open(newfile, "r").read()))
            self.save()
        
    def get_projects(self):
        photopool_items = Pool.objects.filter(photo=self)
        projects = []
        for photopool_item in photopool_items:
            projects.append(photopool_item.content_object)
        return projects
        
    def get_geojson(self):
        c = Context({"type": get_model_name(self),
                "self": self})

        t = Template("""{"type": "{{type}}",\
                "id": "{{self.id}}",\
                "title": "{{self.title}}",\
                "caption": "{{self.caption}}",\
                "date_added": "{{self.date_added|date}} ",\
                "marker_image": "{{self.get_50x50_url}}",\
                {% if self.has_location %}\
                    "location": {% autoescape off %}{{self.location.geojson}}{% endautoescape %},\
                {% endif %}\
                "location_name": "{{self.location_name}}" }""")
        return t.render(c)
        
    get_absolute_url = models.permalink(get_absolute_url)
geo.register(Image)


class Pool(models.Model):
    """
    model for a photo to be applied to an object
    """

    photo           = models.ForeignKey(Image)
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    content_object  = generic.GenericForeignKey()
    created_at      = models.DateTimeField(_('created_at'), default=datetime.now)

    class Meta:
        # Enforce unique associations per object
        unique_together = (('photo', 'content_type', 'object_id'),)
        verbose_name = _('pool')
        verbose_name_plural = _('pools')
