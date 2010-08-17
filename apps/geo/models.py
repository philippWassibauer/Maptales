from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.contrib.auth.models import User
from django.template import Context, Template
import tempfile
from maptales_app.utils import get_model_name
from categories.models import CategorizedItem
import os
from django.contrib.gis.geos import Point, Polygon
from tagging.fields import TagField
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from geo.utils import reverse_geocode
from misc.polymorphic import PolymorphicMetaclass

try:
    import cPickle as pickle
except:
    import pickle

import base64
from maptales_app.models import PRIVACY_LEVELS

MAPSTYLE_SATELLITE = 1
MAPSTYLE_HYBRID = 2
MAPSTYLE_MAP = 3
MAPSTYLE_TERRAIN = 4

MAPSTYLE_CHOICES = (
    (MAPSTYLE_SATELLITE, _('Satellite')),
    (MAPSTYLE_HYBRID, _('Hybrid')),
    (MAPSTYLE_MAP, _('Map')),
    (MAPSTYLE_TERRAIN, _('Terrain')),
)

def get_gmapmode(choice):
    if choice == MAPSTYLE_SATELLITE:
        return "G_SATELLITE_MAP"
    elif choice == MAPSTYLE_HYBRID:
        return "G_HYBRID_MAP"
    elif choice == MAPSTYLE_MAP:
        return "G_NORMAL_MAP"
    elif choice == MAPSTYLE_TERRAIN:
        return "G_PHYSICAL_MAP"


class SerializedDataField(models.TextField):
    """Because Django for some reason feels its needed to repeatedly call
    to_python even after it's been converted this does not support strings."""
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value is None:
            return
        if not isinstance(value, basestring):
            return value
        value = pickle.loads(base64.b64decode(value))
        return value

    def get_db_prep_save(self, value):
        if value is None:
            return
        return base64.b64encode(pickle.dumps(value))

class GeoAbstractModelManager(models.GeoManager):
    def search_in_area(self, x1, y1, x2, y2):
        poly = Polygon.from_bbox((x1, y1, x2, y2))
        return GeoAbstractModel.objects.filter(bbox__bboverlaps=poly)
        
    def search_nearby(self, x, y):
        return GeoAbstractModel.objects.filter(bbox__bboverlaps=poly)
        
class GeoAbstractModel(models.Model):
    content_type   = models.ForeignKey(ContentType,
            related_name="content_type_set_for_%(class)s", null=True,
            blank=True)
    object_id      = models.PositiveIntegerField(_('object ID'), null=True,
                                                 blank=True)
    content_object = generic.GenericForeignKey()
    #metadata = SerializedDataField(blank=True, editable=False)
    objects = GeoAbstractModelManager()
    creation_date      = models.DateTimeField(_('created_at'),
                                              default=datetime.now())
    update_date      = models.DateTimeField(_('updated_at'),
                                            default=datetime.now())
    zoom = models.PositiveIntegerField("zoom", default=10)
    creator = models.ForeignKey(User, related_name="geo_items")
    bbox = models.PolygonField(srid=4326, null=True, blank=True)
    
    __metaclass__ = PolymorphicMetaclass
    
    def post_polymorphic_save(self):
        if self.downcast().get_bbox():
            self.bbox = Polygon.from_bbox(self.downcast().get_bbox())
            
        

class GeoGeometryTag(GeoAbstractModel):
    title         = models.CharField(_('title'), max_length=300, blank=True)
    description     = models.TextField(_('description'), blank=True, null=True)
    geometry_collection = models.GeometryCollectionField(srid=4326)
    objects = models.GeoManager()
    
    def get_bbox(self):
        return self.geometry_collection.extent
        

class GeoLineTag(GeoAbstractModel):
    title         = models.CharField(_('title'), max_length=300, blank=True, null=True)
    description     = models.TextField(_('description'), blank=True, null=True)
    distance        = models.FloatField(_('distance'), default=0)
    line = models.LineStringField(srid=4326)

    from_location_name = models.CharField(_('from location'), max_length=300,
                                          blank=True)
    to_location_name = models.CharField(_('to location'), max_length=300,
                                        blank=True)
    
    def get_bbox(self):
        return self.line.extent
        
    def __unicode__(self):
        return self.title

    def get_geojson(self):
        c = Context({"type": get_model_name(self),
                "title":self.title,
                "creation_date": self.creation_date,
                "update_date": self.update_date,
                "distance": self.distance,
                "creator": self.creator,
                "self": self,
                "line": self.line.geojson})

        t = Template("""{"type": "{{type}}",\
                "id": "{{self.id}}",\
                "title": "{{title|linebreaksbr}}",\
                "description": "{{self.description|linebreaksbr}}",\
                "creation_date": "{{creation_date}}",\
                "update_date": "{{update_date}}",\
                "creator": "{{creator}}",\
                "track": {% autoescape off %}{{line}}{% endautoescape %} }""")
        
        return t.render(c)


class GeoPointTagManager(models.GeoManager):
    def search_in_area(self, x1, y1, x2, y2):
        poly = Polygon.from_bbox((x1, y1, x2, y2))
        return GeoPointTag.objects.filter(location__contained=poly)
        
        
class GeoPointTag(GeoAbstractModel):
    location        = models.PointField(srid=4326)
    location_name   = models.CharField(_('location name'), max_length=300,
                                       blank=True, null=True)
    objects = GeoPointTagManager()
    
    def get_bbox(self):
        return self.location.extent
        
    def save(self, *args, **kwargs):
        if self.location:
            if self.pk is not None:
                orig = GeoPointTag.objects.get(pk=self.pk)
                if orig.location != self.location:
                    self.location_name = reverse_geocode(self.location)
            else:
                self.location_name = reverse_geocode(self.location)
        super(GeoPointTag, self).save(*args, **kwargs)
    
    def get_geojson(self):
        c = Context({"type": get_model_name(self),
                     "self": self})

        t = Template("""{"type": "{{type}}",\
                "id": "{{self.id}}",\
                "location": {{self.location.geojson}}}""")
        return t.render(c)
        

class MGPXTrackManager(models.GeoManager):
    def search_in_area(self, x1, y1, x2, y2):
        poly = Polygon.from_bbox((x1, y1, x2, y2))
        return MGPXTrack.objects.filter(segments__track__bboverlaps=poly)


class MGPXTrack(GeoAbstractModel):
    title           = models.CharField(_('title'), max_length=300, blank=True, null=True)
    description     = models.TextField(_('description'), blank=True, null=True)
    distance        = models.FloatField(_('distance'), default=0)
    start_time = models.DateTimeField(_('start_time'), blank=True, null=True)
    end_time = models.DateTimeField(_('end_time'), blank=True, null=True)
    safetylevel = models.IntegerField(_('safetylevel'), choices=PRIVACY_LEVELS,
                                      default=1,
                                      help_text=_('privacy helptext'))
    
    gpx_file = models.FileField(upload_to="gpx_files", max_length=250)
    
    categories = generic.GenericRelation(CategorizedItem)

    from_location_name = models.CharField(_('from location'), max_length=300,
                                          blank=True)
    to_location_name = models.CharField(_('to location'), max_length=300,
                                        blank=True)

    tags = TagField()
    objects = MGPXTrackManager()
    
    def set_story_reference(self, story):
        self.content_object = story
        self.save()
        for segment in self.segments.all():
            segment.content_object = story
            segment.save()
            
    def get_bbox(self):
        if self.segments.all():
            return self.segments.all()[0].get_bbox()
        
    def get_total_points(self):
        count = 0
        for segment in self.segments.all():
            count = count+len(segment.track.array)
        return count
        
    def get_average_speed(self):
        return self.distance/(self.duration().seconds/60.0/60.0)

    def get_top_speed(self):
        return 0

    def get_vertical_distance(self):
        up = 0
        down = 0
        for segment in self.segments.all():
            (upIn, downIn) = segment.get_vertical_distance()
            up = up+upIn
            down = down+downIn
        return (up, down)

    def get_vertical_up(self):
        return self.get_vertical_distance()[0]

    def get_vertical_down(self):
        return self.get_vertical_distance()[1]

    def duration(self):
        return self.end_time - self.start_time

    def is_single_day(self):
        if (self.end_time - self.start_time).days <= 1:
            if self.end_time.day == self.start_time.day:
                return True
        return False

    def __unicode__(self):
        return self.title

    def get_categories(self):
        return Category.objects.get_for_model(MGPXTrack)

    def get_location(self):
        if self.segments.all():
            track = self.segments.all()[0].track
            index = round(len(track.array)/2)
            return Point(track.array[index][1], track.array[index][0])

    def get_absolute_url(self):
        return ('view_path', None, {
            'id': self.id
    })
    get_absolute_url = models.permalink(get_absolute_url)
    
    def small_list_render(self):
        return mark_safe(render_to_string('geo/gpx_list_render.html',
                                          { 'track': self })) 
    
    def intersecting_tracks(self):
        return MGPXTrack.objects.filter(
                    segments__track__intersects=self.segments__track)\
                    .exclude(pk=self.pk)

    def get_geojson(self):
        segments = []
        for segment in self.segments.all():
            segments.append(segment.get_geojson())
        segments_string = "["+"], [".join(segments)+"]"


        c = Context({"type": get_model_name(self),
                "title": self.title,
                "creation_date": self.creation_date,
                "update_date": self.update_date,
                "distance": self.distance,
                "total_up": self.get_vertical_up(),
                "total_down": self.get_vertical_down(),
                "start_time": self.start_time,
                "end_time": self.end_time,
                "creator": self.creator,
                "self": self,
                "segments": segments_string})
        
        t = Template("""{"type": "{{type}}",\
            "id": "{{self.id}}",\
            "title": "{{title|linebreaksbr}}",\
            "creation_date": "{{creation_date}}",\
            "update_date": "{{update_date}}",\
            "distance": "{{distance}}",\
            "total_up": "{{total_up}}",\
            "total_down": "{{total_down}}",\
            "start_time": "{{start_time}}",\
            "end_time": "{{end_time}}",\
            "creator": "{{creator}}",\
            "segments":{% autoescape off %}{{segments}}{% endautoescape %}}""")
        return t.render(c)


class MGPXTrackSegment(GeoAbstractModel):
    title         = models.CharField(_('title'), max_length=300, blank=True, null=True)
    description     = models.TextField(_('description'), blank=True, null=True)
    distance        = models.FloatField(_('distance'), default=0)
    start_time = models.DateTimeField(_('start_time'), blank=True, null=True)
    end_time = models.DateTimeField(_('end_time'), blank=True, null=True)
    parent =  models.ForeignKey(MGPXTrack, related_name="segments", blank=True,
                                null=True)
    track = models.LineStringField(srid=4326)
    raw_track = SerializedDataField(_('raw_track'), blank=True, null=True)

    from_location_name = models.CharField(_('from location'), max_length=300,
                                          blank=True)
    to_location_name = models.CharField(_('to location'), max_length=300,
                                        blank=True)

    gpx_height_graph = models.ImageField(upload_to="gpx_height_graph")
    objects = models.GeoManager()
    
    def get_bbox(self):
        return self.track.extent
        
    def __unicode__(self):
        if self.title:
            return self.parent.title + " > " + self.title
        else:
            return self.parent.title + " > Segment"

    def get_vertical_distance(self):
        try:
            up = 0
            down = 0
            focus_elevation = None
            for point in self.raw_track:
                if not focus_elevation:
                    focus_elevation = point.elevation
                else:
                    vertical = point.elevation-focus_elevation
                    focus_elevation = point.elevation
                    if vertical <= 0:
                        down = down + vertical
                    else:
                        up = up + vertical
                        
            return (up, down)
        except:
            return (0,0)
        
    def get_vertical_up(self):
        return self.get_vertical_distance()[0]

    def get_vertical_down(self):
        return self.get_vertical_distance()[1]

    def get_geojson(self):
        timestamps = "''"
        altitudes = "''"
        if self.raw_track:
            try:
                timestamps = []
                for point in self.raw_track:
                    if (point["timestamp"]):
                        timestamps.append(point["timestamp"])
                    else:
                        timestamps.append(point.time.strftime("%b %d, %Y %H:%M:%S"))
                timestamps = simplejson.dumps(timestamps)
                altitudes = simplejson.dumps([ point.elevation
                                              for point in self.raw_track])
            except:
                pass
        c = Context({"type": get_model_name(self),
                "title":self.title,
                "creation_date": self.creation_date,
                "update_date": self.update_date,
                "distance": self.distance,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "creator": self.creator,
                "timestamps": timestamps,
                "altitudes": altitudes,
                "total_up": self.get_vertical_up(),
                "total_down": self.get_vertical_down(),
                "self": self,
                "track": self.track.geojson})

        t = Template("""{"type": "{{type}}",\
            "id": "{{self.id}}",\
            "parent_id": "{{self.parent.id}}",\
            "title": "{{title|linebreaksbr}}",\
            "description": "{{self.description|linebreaksbr}}",\
            "creation_date": "{{creation_date}}",\
            "update_date": "{{update_date}}",\
            "distance": "{{distance}}",\
            "total_up": "{{total_up}}", \
            "total_down": "{{total_down}}",\
            "start_time": "{{start_time}}",\
            "end_time": "{{end_time}}",\
            "altitudes": {% autoescape off %}{{altitudes}}{% endautoescape %},\
            "timestamps":{% autoescape off %}{{timestamps}}{% endautoescape %},\
            "creator": "{{creator}}",\
            "track": {% autoescape off %}{{track}}{% endautoescape %} }""")
        return t.render(c)

    def duration(self):
        """Return the duration for this track. The sum of the duration
        of all track segments."""
        return self.end_time-self.start_time

    def render_chart(self, force_insert=False, force_update=False):
        super(MGPXTrackSegment, self).save(force_insert, force_update)
        heightpoints = []
        lowestpoint = None
        highestpoint = None

        for coordinate in self.raw_track:
            if(coordinate.elevation):
                elevation = coordinate.elevation
                if lowestpoint == None or lowestpoint > elevation:
                    lowestpoint = elevation
                if highestpoint == None or highestpoint < elevation:
                    highestpoint = elevation
                heightpoints.append(elevation)
        data = {"track": heightpoints }
        start_time = str(self.start_time.hour)+":"+str(self.start_time.minute)
        h_labels = [start_time, start_time, start_time, start_time]
        try:
            from geo.CairoPlot import dot_line_plot
            file_name = tempfile.mktemp(".png")
            dot_line_plot(file_name, data, 375, 300,
                           h_labels=h_labels, axis=True, grid=True,
                           v_bounds=(lowestpoint-200, highestpoint+200))
            self.gpx_height_graph.save(
                os.path.basename("%s_%s.png"%(self.id, self.title)),
                ContentFile(open(file_name, "r").read()))
        except:
            pass
