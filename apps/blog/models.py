from datetime import datetime

from django.contrib.gis.db import models

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from tagging.models import Tag

from django.contrib.auth.models import User
from photologue.models import ImageModel
from geo.utils import reverse_geocode
from maptales_app.models import PRIVACY_LEVELS
from maptales_app.utils import get_model_name
from django.template import Context, Template
from django.contrib.contenttypes import generic
from geo.models import GeoAbstractModel

try:
    from notification import models as notification
    from django.db.models import signals
except ImportError:
    notification = None

try:
    markup_choices = settings.WIKI_MARKUP_CHOICES  # reuse this for now; taken from wiki
except AttributeError:
    markup_choices = (
        ('rst', _(u'reStructuredText')),
        ('txl', _(u'Textile')),
        ('mrk', _(u'Markdown')),
    )

class PostImage(ImageModel):
    post = models.OneToOneField('Post', primary_key=True, related_name="postimage")

class Post(models.Model):
    """
    Post model.
   """
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    title           = models.CharField(_('title'), max_length=200)
    slug            = models.SlugField(_('slug'), max_length=200, unique=True)
    author          = models.ForeignKey(User, related_name="added_posts")
    creator_ip      = models.IPAddressField(_("IP Address of the Post Creator"), blank=True, null=True)
    tease           = models.TextField(_('tease'), blank=True)
    body            = models.TextField(_('body'))
    status          = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    allow_comments  = models.BooleanField(_('allow comments'), default=True)
    publish         = models.DateTimeField(_('publish'), default=datetime.now)
    created_at      = models.DateTimeField(_('created at'), default=datetime.now)
    updated_at      = models.DateTimeField(_('updated at'), default=datetime.now)
    markup          = models.CharField(_(u"Post Content Markup"), max_length=3,
                              choices=markup_choices,
                              default='txl',
                              null=True, blank=True)
    views           = models.IntegerField(editable=False, default=0)
    tags            = TagField()

    safetylevel = models.IntegerField(_('safetylevel'), choices=PRIVACY_LEVELS, default=1,  help_text=_('Who can read this Post?'))
    
    #objects = models.GeoManager()
    
    class Meta:
        verbose_name        = _('post')
        verbose_name_plural = _('posts')
        ordering            = ('-publish',)
        get_latest_by       = 'publish'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('blog_post', None, {
            'username': self.author.username,
            'slug': self.slug
    })
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_geojson(self):
        c = Context({"type": get_model_name(self),
                "self": self,
                "STATIC_URL": settings.STATIC_URL})

        t = Template("""{"type": "{{type}}",\
                "id": "{{self.id}}",\
                "title": "{{self.title}}",\
                "body": "{{self.body}}",\
                "publish": "{{self.publish|date}} ",\
                "marker_image": "{{STATIC_URL}}/images/post-75-75.gif",\
                "slug": "{{self.slug}}",\
                {% if self.has_location %}\
                    "location": {% autoescape off %}{{self.location.geojson}}{% endautoescape %},\
                {% endif %}\
                "location_name": "{{self.location.location_name}}" }""")
        return t.render(c)
        
import geo
geo.register(Post)


# handle notification of new comments
from threadedcomments.models import ThreadedComment
def new_comment(sender, instance, **kwargs):
    if isinstance(instance.content_object, Post):
        post = instance.content_object
        if notification:
            notification.send([post.author], "blog_post_comment", {"user": instance.user, "post": post, "comment": instance})
signals.post_save.connect(new_comment, sender=ThreadedComment)
