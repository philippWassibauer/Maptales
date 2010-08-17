from django.template import Library
from django.conf import settings
from geo.models import MGPXTrack
register = Library()
from geo.forms import LocationInputForm
from django.shortcuts import get_object_or_404, render_to_response
from native_tags.decorators import function, comparison, filter
from django.template.loader import render_to_string
from geo.models import GeoAbstractModel, GeoPointTag
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from misc.utils import get_target_contenttype
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Max, Min, Count
from django.contrib.auth.models import User
from django.template import RequestContext

def items_in_area():
    return "ddddddd"
items_in_area = function(items_in_area)



def get_users_tracks(user):
    return MGPXTrack.objects.filter(creator=user).order_by("-creation_date")
get_users_tracks = function(get_users_tracks)    


def show_users_clustermap(user, content_type=None, request=None):
    return render_to_string("geo/user_cluster_widget.html", {
        "user": user,
    }, context_instance=RequestContext(request))
show_users_clustermap = function(show_users_clustermap)

def list_countries(template_name="geo/country_list.html"):
    from natural_earth.models import Country
    if cache.get("countries"):
        return cache.get("countries")
    else:
        cached_template =render_to_string(template_name, {
            "countries": Country.objects.all().values(),
        })
        cache.set("countries", cached_template, 60*60*24)
        return cached_template
list_countries = function(list_countries)


def country_selector(selected_country=None, template_name="geo/country_selector.html"):
    from natural_earth.models import Country
    cache_name = "country_selector_%s"%selected_country
    if cache.get(cache_name):
        return cache.get(cache_name)
    else:
        cached_template =render_to_string(template_name, {
            "countries": Country.objects.all().values(),
            "selected_country": selected_country,
        })
        cache.set(cache_name, cached_template, 60*60*24)
        return cached_template
country_selector = function(country_selector)  
    
    
def tagcloud_of_area(x1, y1, x2, y2):
    from geo.utils import tag_usage_for_queryset
    tags = tag_usage_for_queryset(GeoAbstractModel.objects\
                                      .search_in_area(x1, y1, x2, y2), True, 8)
    return render_to_string("geo/geotagcloud.html", {
        "tags": tags,
    })
tagcloud_of_area = function(tagcloud_of_area)


def objects_in_area(contenttype, x1, y1, x2, y2, template_name="geo/objects_in_area.html", offset=0, count=40, ordering="creation_date"):
    content_type = get_target_contenttype(contenttype)
    items = GeoAbstractModel.objects.search_in_area(x1, y1, x2, y2).filter(content_type=content_type)[offset:(offset+count)]
    
    items = items.order_by(ordering)
    
    return render_to_string(template_name, {
        "items": items,
    })
objects_in_area = function(objects_in_area)


def users_objects_in_area(users, x1, y1, x2, y2, contenttype=None, template_name="geo/objects_in_area.html", offset=0, count=40, ordering="creation_date"):
    content_type = get_target_contenttype(contenttype)
    items = GeoAbstractModel.objects.search_in_area(x1, y1, x2, y2)
    if content_type:
        items = items.filter(content_type=content_type)
    if users:
        items = item.filter(creator__in=users)
        
    items = items.order_by(ordering)
    
    return render_to_string(template_name, {
        "items": items[offset:(offset+count)],
    })
objects_in_area = function(objects_in_area)



def users_in_area(x1, y1, x2, y2, template_name="geo/users_in_area.html", offset=0, count=4):
    items = GeoAbstractModel.objects.search_in_area(float(x1), float(y1), float(x2), float(y2)).values("creator").annotate(creator_count=Count("creator")).order_by("-creator_count")[offset:(offset+count)]
    for item in items:
        item['creator'] = User.objects.get(pk=item['creator'])
        
    return render_to_string(template_name, {
        "items": items,
    })
users_in_area = function(users_in_area)


def nearest_postings(object, template_name="geo/nearby.html", offset=0, count=5):
    #import pdb; pdb.set_trace()
    from django.contrib.gis.measure import D
    point = GeoPointTag.objects.get(content_type=ContentType.objects.get_for_model(object),
                                         object_id=object.pk)
    items = GeoPointTag.objects.exclude(object_id=object.pk)
    items = items.distance("POINT("+str(point.location.x)+" "+str(point.location.y)+")", field_name="location")
    items = items.order_by("distance")
    return render_to_string(template_name, {
        "items": items[offset:(offset+count)],
    })
nearest_postings = function(nearest_postings)


@register.inclusion_tag("geo/show_overal_location.html")
def show_overal_location(item_to_show):
    bbox = None
    if hasattr(item_to_show, "location"):
        location = item_to_show.location
    else:
        from story.models import Story
        if isinstance(item_to_show, MGPXTrack):
            location = item_to_show.get_location()
        elif isinstance(item_to_show, Story):
            location = item_to_show.get_center_location()
            bbox = item_to_show.bbox
        else:
            location = None
            
    return {"location_input_form": LocationInputForm().fields["location"].widget.render("location", location, attrs={"item_to_place":item_to_show}),
            "location": location,
            "bbox": bbox,
            "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY}


@register.inclusion_tag("geo/location_autocomplete.html")
def location_autocomplete(callback_function):
     return {"callback_function":callback_function}
