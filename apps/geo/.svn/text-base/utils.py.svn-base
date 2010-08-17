import sys, string
from django.contrib.gis.geos import LineString, Point, Polygon
from geo.pygpx import GPX, GPXTrack
from geopy.geocoders.google import Google
from geopy.point import Point
from django.conf import settings
import logging
import traceback
import sys
import traceback, pprint
from django.contrib.auth.models import User

from tagging.models import TaggedItem, Tag
from django.contrib.contenttypes.models import ContentType
from tagging.utils import calculate_cloud
from tagging.utils import LOGARITHMIC
from django.db import connection
qn = connection.ops.quote_name


def convert_gpx_point_to_point(tracksegent):
    if tracksegent.elevation:
        return (tracksegent.lon, tracksegent.lat)
    else:
        return (tracksegent.lon, tracksegent.lat)
    
def convert_gpx_json_point_to_point(tracksegent):
    if hasattr(tracksegent, "elevation"):
        return (float(tracksegent["lon"]), float(tracksegent["lat"]))
    else:
        return (float(tracksegent["lon"]), float(tracksegent["lat"]))
    
def convert_gpx_segment_to_linestring(tracksegment):
    points = [convert_gpx_point_to_point(point) for point in tracksegment ]
    return LineString(points)


def convert_mobile_app_to_linestring(jsontracking):
    points = [convert_gpx_json_point_to_point(point) for point in jsontracking ]
    return LineString(points)

def convert_gpx_file(gpx_file, gpxTrack):
    from geo.models import MGPXTrackSegment
    gpx = GPX(gpx_file)
    for trk in gpx.tracks:
        if not gpxTrack.title:
            gpxTrack.title = trk.name
        gpxTrack.distance = trk.distance() / 1000.0
        gpxTrack.start_time = trk.start_time()
        gpxTrack.end_time = trk.end_time()
        gpxTrack.save()
        for segment in trk.trksegs:
            track = convert_gpx_segment_to_linestring(segment.trkpts)
            gpxTrackSegment = MGPXTrackSegment(raw_track=segment.trkpts,
                                               creator=gpxTrack.creator,
                                               track=track, parent=gpxTrack,
                                               distance=track.length,
                                               start_time = segment.trkpts[0].time,
                                               end_time = segment.trkpts[-1].time)
            gpxTrackSegment.save()
    gpxTrack.save()
    return gpxTrack


def reverse_geocode(point):
    try:
        g = Google(settings.GOOGLE_MAPS_API_KEY)
        (new_place,new_point) = g.reverse((point.y, point.x))
        return new_place
    except:
        pass
    return ""   


def geocode(name, exactly_one=False):
    try:
        g = Google(settings.GOOGLE_MAPS_API_KEY)
        return list(g.geocode(name, exactly_one=exactly_one))
    except:
        logging.error("Could not get reverse geocode for {{point.y}}-{{point.x}}")

        
def get_tags_in_area(x1, y1, x2, y2):
    pass


def tag_usage_for_queryset(queryset, counts=False, min_count=None):
        """
        Obtain a list of tags associated with instances of a model
        contained in the given queryset.

        If ``counts`` is True, a ``count`` attribute will be added to
        each tag, indicating how many times it has been used against
        the Model class in question.

        If ``min_count`` is given, only tags which have a ``count``
        greater than or equal to ``min_count`` will be returned.
        Passing a value for ``min_count`` implies ``counts=True``.
        """
        
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
        return _tag_usage_for_queryset(queryset.model, counts, min_count,
                                       extra_joins, extra_criteria, params)


def _tag_usage_for_queryset(model, counts=False, min_count=None, extra_joins=None,
                            extra_criteria=None, params=None):
        from tagging.models import Tag
        """
        Perform the custom SQL query for ``usage_for_model`` and
        ``usage_for_queryset``.
        """
        if min_count is not None: counts = True
        
        model_table = qn(model._meta.db_table)
        model_pk = '%s.%s' % (model_table, "object_id")
        query = """
        SELECT DISTINCT %(tag)s.id, %(tag)s.name%(count_sql)s
        FROM
            %(tag)s
            INNER JOIN %(tagged_item)s
                ON %(tag)s.id = %(tagged_item)s.tag_id
            INNER JOIN %(model)s
                ON %(tagged_item)s.object_id = %(model_pk)s
            %%s
        WHERE %(tagged_item)s.content_type_id = %(model)s.content_type_id
            %%s
        GROUP BY %(tag)s.id, %(tag)s.name
        %%s
        ORDER BY %(tag)s.name ASC""" % {
            'tag': qn(Tag._meta.db_table),
            'count_sql': counts and (', COUNT(%s)' % model_pk) or '',
            'tagged_item': qn(TaggedItem._meta.db_table),
            'model': model_table,
            'model_pk': model_pk,
        }
        
        min_count_sql = ''
        if min_count is not None:
            min_count_sql = 'HAVING COUNT(%s) >= %%s' % model_pk
            params.append(min_count)

        cursor = connection.cursor()
        cursor.execute(query % (extra_joins, extra_criteria, min_count_sql), params)
        
        tags = []
        for row in cursor.fetchall():
            t = Tag(*row[:2])
            if counts:
                t.count = row[2]
            tags.append(t)
            
        return calculate_cloud(tags, 4, LOGARITHMIC)
    
    
def get_active_users_in_area(x1, y1, x2, y2):
    # users that have either placed an item here, or uploaded gpx
    from geo.models import GeoAbstractModel
    from django.db.models import Count
    poly = Polygon.from_bbox((x1, y1, x2, y2))
    user_data = GeoAbstractModel.objects.filter(bbox__bboverlaps=poly)\
                        .values('creator')\
                        .annotate(counter=Count('creator')).order_by('-counter')[0:20]
    return [{"counter":user['counter'], "user": User.objects.get(pk=user['creator'])}
                for user in user_data]


def get_from_country(object_type, country_name):
    from natural_earth.models import Country as NECountry
    MGPXTrackSegment.objects.filter(track__contained=NECountry.objects.get(name__contains="Slovakia").mpoly)


def social_query(user, network, total_q):
    users = None
    if user:
        if network:
            from activity_stream.models import get_people_i_follow
            users = get_people_i_follow(user, 1000)
        else:
            users = [user]
    if users:
        total_q = total_q.filter(creator__in=users)
    
    return total_q