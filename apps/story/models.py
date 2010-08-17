from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from maptales_app.utils import get_model_name
from geo.models import MGPXTrack

from datetime import datetime
from positions.fields import PositionField
from django.template import Context, Template
from photologue.models import ImageModel
from maptales_app.models import PRIVACY_LEVELS
from geo.models import MAPSTYLE_CHOICES, get_gmapmode
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from categories.models import Category, CategorizedItem
from django.contrib.gis.geos import Point, Polygon
from geo.models import GeoAbstractModel, GeoPointTag
from django.db import connection

qn = connection.ops.quote_name

def stories_in_geo_queryset(queryset):
        if getattr(queryset.query, 'get_compiler', None):
            # Django 1.2+
            compiler = queryset.query.get_compiler(using='default')
            extra_joins = ' '.join(compiler.get_from_clause()[0][1:])
            where, params = queryset.query.where.as_sql(
                compiler.quote_name_unless_alias, compiler.connection
            )
        else:
            # Django pre-1.2
            extra_joins = ' '.join(queryset.query.get_from_clause()[0][1:])
            where, params = queryset.query.where.as_sql()
        
        if where:
            extra_criteria = 'AND %s' % where
        else:
            extra_criteria = ''
        return _stories_in_geo_queryset(queryset.model, extra_joins, extra_criteria, params)


def _stories_in_geo_queryset(model, extra_joins, extra_criteria, params):
    model_table = qn(model._meta.db_table)
    model_pk = '%s.%s' % (model_table, "object_id")
    query = """
    SELECT DISTINCT %(story)s.id
    FROM
        %(story)s
        INNER JOIN %(story_line_item)s
            ON %(story)s.id = %(story_line_item)s.story_id
        INNER JOIN %(model)s
            ON %(story_line_item)s.id = %(model_pk)s
        %%s
    WHERE %(story)s.id = %(story)s.id
        %%s
    """ % {
        'story': qn(Story._meta.db_table),
        'story_line_item': qn(StoryLineItem._meta.db_table),
        'model': model_table,
        'model_pk': model_pk,
    }

    cursor = connection.cursor()
    cursor.execute(query % (extra_joins, extra_criteria), params)
    
    ids = []
    for row in cursor.fetchall():
        ids.append(row[0])
        
    return Story.objects.filter(pk__in=ids)
    
class StoryImage(ImageModel):
    story = models.OneToOneField('Story', primary_key=True,
                                 related_name="storyimage")


class StoryManager(models.GeoManager):
    def search_in_area(self, x1, y1, x2, y2):
        poly = Polygon.from_bbox((x1, y1, x2, y2))
        return stories_in_geo_queryset(GeoAbstractModel.objects\
                                      .search_in_area(x1, y1, x2, y2).filter(content_type=ContentType.objects.get_for_model(StoryLineItem)))
        
    def nearby(self, x, y, exclude_story=None):
        qs = GeoPointTag.objects.distance("POINT("+str(x)+" "+str(y)+")", field_name="location")
        qs = qs.order_by("distance")
        abstract_table_name = GeoAbstractModel._meta.db_table
        point_tag_name = GeoPointTag._meta.db_table
        content_type_id = ContentType.objects.get_for_model(StoryLineItem).pk
        
        qs = qs.extra(tables=[abstract_table_name],
                       where=['%s.content_type_id = %s AND %s.id = %s.geoabstractmodel_ptr_id'%(abstract_table_name,content_type_id, abstract_table_name, point_tag_name)])

        stories = []
        filtered_stories = [exclude_story]
        for item in qs[0:20]:
            if not item.content_object.story in filtered_stories:
                stories.append(item.content_object.story)
                filtered_stories.append(item.content_object.story)
        return stories
        
        
class Story(models.Model):
    STATUS_DRAFT = 1
    STATUS_PUBLIC = 2
    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_PUBLIC, _('Public')),
    )

    title           = models.CharField(_('title'), max_length=300, blank=True)
    slug            = models.SlugField(_('slug'), max_length=300, unique=True, blank=True, null=True)
    creator         = models.ForeignKey(User, related_name="stories")
    
    description     = models.TextField(_('description'), blank=True, null=True)

    status          = models.IntegerField(_('status'), choices=STATUS_CHOICES,
                                          default=1,
                                          help_text=_("status helptext"),
                                          blank=True, null=True)
    
    privacy         = models.IntegerField(_('privacy'), choices=PRIVACY_LEVELS,
                                          default=1,
                                          help_text=_("privacy helptext"),
                                          blank=True, null=True)

    mapmode         = models.IntegerField(_('mapstyle'),
                                          choices=MAPSTYLE_CHOICES, default=1,
                                          blank=True, null=True)

    creation_date   = models.DateTimeField(default=datetime.now())
    update_date     = models.DateTimeField(default=datetime.now())

    from_location_name = models.CharField(_('from location name'),
                                          max_length=300, blank=True)
    
    to_location_name = models.CharField(_('to location name'),
                                        max_length=300, blank=True)
    
    categories = generic.GenericRelation(CategorizedItem)
    
    bbox = models.PolygonField(srid=4326, null=True, blank=True)
    
    objects = StoryManager()
    
    def get_image(self):
        from photos.models import Image
        image_type = ContentType.objects.get_for_model(Image)
        storylineitem = self.storyline.filter(attachments__content_type=image_type).all()
        if storylineitem:
            storylineitem = storylineitem[0]
        imageattachments = [ item.content_object for item in storylineitem.attachments.all() if item.content_type==image_type ]
        return imageattachments
    
    def rearrange_storyline_by_timestamps(self):
        pass

    @property
    def lines(self):
        from geo.models import GeoLineTag
        type = ContentType.objects.get_for_model(self)
        return GeoLineTag.objects.filter(content_type=type,object_id=self.pk)
        
    @property
    def gpx_paths(self):
        from geo.models import MGPXTrackSegment
        type = ContentType.objects.get_for_model(self)
        return MGPXTrackSegment.objects.filter(content_type=type,object_id=self.pk)
        
    def big_img_teaser(self):
        return mark_safe(render_to_string('story/big_pic_teaser.html', { 'story': self }))
        
    def book_teaser(self):
        return mark_safe(render_to_string('story/book_teaser.html', { 'story': self }))
        
    def get_absolute_url(self):
        return ('story_view', None, {
            'slug': self.slug
        })
        
    def get_gmap_mode(self):
        return get_gmapmode(self.mapmode)
        
    def get_duration(self):
        return 20;

    def get_distance(self):
        #import pdb; pdb.set_trace()
        distance = 0
        for track in self.gpx_paths:
            distance += track.distance
        return distance*100
        
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return self.title

    def is_single_day(self):
        if (self.end_time - self.start_time).days <= 1:
            if self.end_time.day == self.start_time.day:
                return True
        return False

    def get_center_location(self):
        if self.bbox:
            return self.bbox.centroid
        else:
            return None
    
    def get_bounding_box(self):
        xmin = ymin = xmax = ymax = None
        for item in self.storyline.all():
            if item.location and item.location.x and item.location.y:
                if xmin == None or item.location.x < xmin:
                    xmin = item.location.x
                if ymin == None or item.location.y < ymin:
                    ymin = item.location.y
                if xmax == None or item.location.x > xmax:
                    xmax = item.location.x
                if ymax == None or item.location.y > ymax:
                    ymax = item.location.y
        return (xmin, ymin, xmax, ymax)
    
    def export_timestamps_to_js(self):
        timestamps = []
        counter = 0
        for path in self.gpx_paths:
            for point in path.raw_track:
                timestamps.append(str(counter))
                counter = counter+1
        return "[%s]"%(",".join(timestamps))

    def export_altitude_to_js(self):
        altitude = []
        for path in self.gpx_paths:
            for point in path.raw_track:
                try:
                    if point["altitude"]>="0":
                        altitude.append(point["altitude"])
                    else:
                        altitude.append("0") 
                except:
                    altitude.append("0")   
                       
        return "[%s]"%(",".join(altitude))

    def export_speed_to_js(self):
        speeds = []
        for path in self.gpx_paths:
            for point in path.raw_track:
                try:
                    if point["speed"]>="0":
                        speeds.append(str(float(point["speed"])*3.6))
                    else:
                        speeds.append("0")
                except:
                    speeds.append("0") 
        return "[%s]"%(",".join(speeds))

    def save(self, *args, **kwargs):
        (xmin, ymin, xmax, ymax) = self.get_bounding_box()
        if xmin != None and ymin != None and xmax != None and ymax != None:
            self.bbox = Polygon.from_bbox((xmin, ymin, xmax, ymax))
        super(Story, self).save(*args, **kwargs)


class StoryLineItem(models.Model):
    story = models.ForeignKey(Story, related_name='storyline', db_index=True)
    text = models.TextField()
    creator = models.ForeignKey(User, related_name="storylineitems")
    position = PositionField(collection='story')
    creation_date = models.DateTimeField(default=datetime.now())
    update_date = models.DateTimeField(default=datetime.now())
    timestamp_start = models.DateTimeField(default=datetime.now())
    timestamp_end = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.text
    
    def get_length_indicator(self):
        if len(self.text) < 100:
            return 100
        if len(self.text) < 200:
            return 200
        if len(self.text) < 300:
            return 300
        
        return 400
        
    def get_image(self):
        from photos.models import Image
        image_type = ContentType.objects.get_for_model(Image)
        return self.attachments.filter(content_type=image_type)

    class Meta:
        # Enforce unique associations per object
        ordering = ('position',)
        
    def get_previous_by_position(self):
        item = StoryLineItem.objects.filter(story=self.story, position__lt=self.position).order_by("-position")[0:1]
        if item:
            return item[0]
        else:
            return None
        
        
    def get_next_by_position(self):
        item = StoryLineItem.objects.filter(story=self.story, position__gt=self.position).order_by("position")[0:1]
        if item:
            return item[0]
        else:
            return None

    def get_geojson(self):
        c = Context({"type": get_model_name(self),
                "story":self.story,
                "self": self,
                "position": self.position})

        t = Template("""{"type": "{{type}}",\
                "id": {{self.id}},\
                "storyId": {{story.id}},\
                "text": "{{self.text|linebreaksbr}}",\
                "marker_image": "{{self.get_image.0.content_object.get_50x50_url}}",\
                {% if self.has_location %}\
                    "location": {% autoescape off %}{{self.location.geojson}}{% endautoescape %},\
                {% endif %}\
                "position": {{position}} }""")
        return t.render(c)
        
import geo
geo.register(StoryLineItem)    
    
class StoryLineItemMedia(models.Model):
    storylineitem   = models.ForeignKey(StoryLineItem, related_name='attachments', db_index=True)
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    content_object  = generic.GenericForeignKey()
    position = PositionField(collection='storylineitem')
    
    class Meta:
        # Enforce unique associations per object
        unique_together = (('content_type', 'object_id', 'storylineitem'),)
        ordering = ('position',)
        
    def __unicode__(self):
        return str(self.storylineitem)+" > "+str(self.content_object)+" > " + str(self.position)

    