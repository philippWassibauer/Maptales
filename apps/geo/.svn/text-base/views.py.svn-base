from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.gis.geos import LineString, Point
from django.utils import simplejson
import logging
from geo.models import MGPXTrack, GeoPointTag, GeoLineTag, GeoAbstractModel
from django.utils.translation import ugettext_lazy as _
import sys

from geo.forms import *
from geo.utils import geocode as geocode_geopy
from activity_stream.models import create_activity_item
from natural_earth.models import Country
from ebgeo.utils.clustering.shortcuts import cluster_all_geoitems
from misc.utils import get_target_contenttype
from utils import social_query
 
@login_required
def place_item(request):
    
    if not request.POST.get("content_type", False) \
        or not request.POST.get("content_object_id", False):
        return HttpResponse(status=400,
                            content="content_type and content_object_id\
                                    are mandatory parameters")
        
    if not request.POST.get("lng", False) \
        or not request.POST.get("lat", False):
        return HttpResponse(status=400,
                            content="lat and lng \
                                    are mandatory parameters")
        
    target_object = get_target_object(request.POST.get("content_type"), 
                                      request.POST.get("content_object_id"))
    
    data = {}
    if float(request.POST.get("lng"))<180\
        and float(request.POST.get("lng"))>-180\
        and float(request.POST.get("lat"))<90\
        and float(request.POST.get("lat"))>-90:
        
        content_type = ContentType.objects.get_for_model(target_object)
        points = GeoPointTag.objects.filter(content_type=content_type,
                                          object_id=target_object.pk,
                                          creator=request.user)
        
        location = Point((float(request.POST.get("lng")),
                          float(request.POST.get("lat"))))
            
        if points and points[0]:
            point = points[0]
            point.location = location
            point.save()
        else:
            #create_activity_item("placed", request.user, target_object)
            GeoPointTag.objects.create(content_type=content_type,
                                          object_id=target_object.pk,
                                          location=location,
                                          creator=request.user)
        

        data["type"] = "success"
        data["code"] = 1
        data["item"] = target_object.get_geojson()
        return HttpResponse(simplejson.dumps(data), status=200,
                            mimetype='application/json')
    else:
        data["type"] = "error"
        data["code"] = -1
        data["message"] = "Lat Lng outside bounding box"
        return HttpResponse(simplejson.dumps(data), status=400,
                                    mimetype='application/json')
        

def get_target_object(content_type, content_object_id):
    content_type_split = content_type.split(".")
    content_type = get_object_or_404(ContentType,
                                     app_label=content_type_split[0],
                                     name=content_type_split[1].replace("_", " "))
    target_object = content_type.get_object_for_this_type (pk=content_object_id)
    return target_object


@login_required 
def your_paths(request, template_name="geo/your_paths.html"):
    paths = MGPXTrack.objects.filter(creator=request.user)\
        .order_by("-creation_date")
    lines = GeoLineTag.objects.filter(creator=request.user)\
        .order_by("-creation_date")
    return render_to_response(template_name, {
        "paths": paths,
        "lines": lines,
    }, context_instance=RequestContext(request))


@login_required   
def upload_gpx(request, template_name="geo/upload.html",
                                                        redirect_to_path=False):
    form = GPXUploadForm(request.user)
    if request.method == "POST":
        form = GPXUploadForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            track = form.save()
            if redirect_to_path:
                return HttpResponseRedirect(reverse("edit_path",
                                                    args=(track.id,)))
            else:
                return HttpResponse(status=200, content=track.get_geojson(),
                                    mimetype='application/json')
    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def edit_path(request, id, template_name="geo/edit_path.html"):
    path = get_object_or_404(MGPXTrack, id=id)
    if request.POST:
        form = GPXEditForm(request.user, request.POST, instance=path)
        if form.is_valid():
            form.save()
            return HttpResponse("<div class='ajax-message'>Successfully stored \
                                Changes</div>",
                                status=200)
    else:
        form = GPXEditForm(request.user, instance=path)
        return render_to_response(template_name, {
            "path": path,
            "track_form":form,
            #"segment_forms":
        }, context_instance=RequestContext(request))


@login_required
def track_selector_list(request, username,
                                        template_name="geo/ajax_gpx_list.html"):
    
    user = get_object_or_404(User, username=username)
    if request.user == user:
        tracks = MGPXTrack.objects.filter(creator=user)
        dynamic_div = 'dynamic_track_list_div'
        ref_url = reverse('track_selector_list',args=(username,))
        callback = request.GET.get("callback", None)
        return render_to_response(template_name, {
                                                  "viewed_user": user,
                                                  "tracks": tracks,
                                                  "callback_function": callback,
                                                  "ref_url": ref_url,
                                                  "dynamic_div": dynamic_div
                                                },
                                      context_instance=RequestContext(request))
    else:
        return HttpResponse(status=400, content="You can only \
                                                    view your own gps tracks")
    
    
def view_path(request, id, template_name="geo/view_path.html"):
    path = get_object_or_404(MGPXTrack, id=id)
    return render_to_response(template_name, {
        "path": path,
    }, context_instance=RequestContext(request))


@login_required
def ajax_update_path(request, id):
    path = get_object_or_404(MGPXTrack, id=id)
    return HttpResponse(status=400, content="Could not parse GPX")


@login_required
def delete_path(request, id, template_name="geo/delete_path.html"):
    path = get_object_or_404(MGPXTrack, id=id)
    if(path.creator==request.user):
        path.delete()
        request.user.message_set.create(message="Successfully \
                                                             deleted GPX Track")
        return HttpResponseRedirect(reverse("your_paths",))
    else:
        return render_to_response("error.html", {
           "title": _("Rights Error"),
           "message": _("Only the creator can delete GPX paths")
        }, context_instance=RequestContext(request))


def browse(request, template_name="geo/browse.html", extra_context={}):
    count = request.POST.get("count", 1000)
    offset = request.POST.get("offset", 0)
    
    if extra_context.get("lat", False):
        lat = extra_context["lat"]
    else:
        lat = request.GET.get("lat", 32.54681317351516)
    
    if extra_context.get("lng", False):
        lng = extra_context["lng"]
    else:
        lng = request.GET.get("lng", -6.328125)
        
    
    if extra_context.get("place", False):
        place = extra_context["place"]
    else:
        place = request.GET.get("place", False)
    
    if extra_context.get("zoom", False):
        zoom = extra_context["zoom"]
    else:
        zoom = request.GET.get("zoom", 2)
        
    total_q = GeoAbstractModel.objects.search_in_area(-90, -90, 90, 90)
    
    total_count = total_q.count()
    total = total_q[offset:count]
    
    #clusters = cluster_all_geoitems(total, 4)
    
    viewed_user = None
    if request.GET.get("user_id", False):
        viewed_user = get_object_or_404(User, pk=request.GET.get("user_id", False))
        
    template_params = {
       "viewed_user": viewed_user,
       "map_position": {"lat": lat, "lng": lng, "zoom": zoom},
       "place": place,
       #"clusters":clusters,
       "total_size": total_count,
       "offset": offset,
       "count": count,
       "lat": lat,
       "lng": lng,
       "zoom": zoom,
    }
    template_params.update(extra_context)
    return render_to_response(template_name, template_params,
                              context_instance=RequestContext(request))

  
def country(request, country_name, template_name="geo/browse.html",
                                                              extra_context={}):
    zoom = request.GET.get("z", 5)
    from natural_earth.models import Country
    country = get_object_or_404(Country, slug=country_name)
    extent = country.mpoly.extent
    
    parameters = {"lat": country.mpoly.centroid.y,
                "lng": country.mpoly.centroid.x,
                "zoom": zoom,
                "selected_country": country}
    parameters.update(extra_context)
    return browse(request, extra_context=parameters)
       
       
def get_clusters(request):
    count = request.POST.get("count", 1000)
    offset = request.POST.get("offset", 0)
    zoom_level = request.POST.get("zoom", 2)
    x1 = request.POST.get("x1", False)
    x2 = request.POST.get("x2", False)
    y1 = request.POST.get("y1", False)
    y2 = request.POST.get("y2", False)
    
    
    total_q = GeoAbstractModel.objects.search_in_area(float(x1),
                                                    float(y1),
                                                    float(x2),
                                                    float(y2))
    
    user_id = request.POST.get("user_id", False)
    network = request.POST.get("network", False)
    if user_id:
        total_q = social_query(get_object_or_404(User, pk=user_id), network, total_q)
    
    total_count = total_q.count()
    total = total_q[offset:count]
    
    clusters = cluster_all_geoitems(total, int(zoom_level)+3)
    
    for cluster in clusters:
        pass
        #cluster.set_overlay_html = 
    
    data = {}
    data["type"] = "success"
    data["code"] = 1
    data["clusters"] = [cluster.get_data() for cluster in clusters]
    return HttpResponse(simplejson.dumps(data), status=200,
                        mimetype='application/json')
    
    
def users_in_area(request,  template_name="", extra_context={}):
    from templatetags.geo_tags import users_in_area
    x1 = request.POST.get("x1", False)
    x2 = request.POST.get("x2", False)
    y1 = request.POST.get("y1", False)
    y2 = request.POST.get("y2", False)
    return HttpResponse(content=users_in_area(x1,y1,x2,y2), status=200)

def get_tags_in_area(request, template_name="", extra_context={}):
    from templatetags.geo_tags import tagcloud_of_area
    x1 = request.POST.get("x1", False)
    x2 = request.POST.get("x2", False)
    y1 = request.POST.get("y1", False)
    y2 = request.POST.get("y2", False)
    return HttpResponse(content=tagcloud_of_area(x1,y1,x2,y2), status=200)

def ajax_browse(request, content_type=None, template_name="", extra_context={}):
    x1 = request.POST.get("x1", False)
    x2 = request.POST.get("x2", False)
    y1 = request.POST.get("y1", False)
    y2 = request.POST.get("y2", False)
    
    offset = request.POST.get("offset", 0)
    count = request.POST.get("count", 14)
    
    if content_type==None:
        content_type = request.POST.get("content_type", None)
        
    items = GeoPointTag.objects.search_in_area(float(x1), float(y1), float(x2), float(y2))
    
    user_id = request.POST.get("user_id", False)
    network = request.POST.get("network", False)
    if user_id:
        items = social_query(get_object_or_404(User, pk=user_id), network, items)
    
    if(content_type):
        content_type = get_target_contenttype(content_type)
        items = items.filter(content_type=content_type)
    
    return render_to_response(template_name, {
       "items": items[offset:(offset+count)],
    }, context_instance=RequestContext(request))
    
  
def geocode(request):
    name = request.GET.get("q", False)
    if name:
        places = geocode_geopy(name, exactly_one=False)
        if places:
            places_out = [{"place": place[0], "lat": place[1][0],
                           "lng": place[1][1]} for place in places]
        else:
            places_out = []
        return render_to_response("geo/autocomplete_response.html", {
           "places": places_out,
        }, context_instance=RequestContext(request))
    else:
        return render_to_response("error.html", {
           "title": _("Geocode Error"),
           "message": _("No Query passed")
        }, context_instance=RequestContext(request))


def get_my_ip():
    """
    Fetch an IP when request.META returns localhost
    """
    import re
    import urllib2
    checkip = urllib2.urlopen('http://checkip.dyndns.org/').read()
    matcher = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    try:
        remote_ip = matcher.search(checkip).group()
    except:
        remote_ip = ''
    return remote_ip


def find_users_near_me(request):
    from django.contrib.gis.utils.geoip import GeoIP
    g = GeoIP()
    remote_ip = request.META['REMOTE_ADDR']
    if remote_ip == '127.0.0.1':
        remote_ip = get_my_ip()
    remote_location = g.city(remote_ip)
    map_position = {}
    map_position['lat'] = remote_location['latitude']
    map_position['lng'] = remote_location['longitude']
    map_position['zoom'] = 11
    return render_to_response("geo/find_users_near_me.html", {
       "city": remote_location['city'],
       "map_position": map_position,
    }, context_instance=RequestContext(request))


def update_line(request):
    line = get_object_or_404(GeoLineTag, pk=request.POST.get("id"))
    if request.POST:
        form = GeoLineTagUpdateForm(request.POST, instance=line)
        if form.is_valid():
            if request.user == line.creator:
                line = form.save(request.user)
                data = {}
                data["type"] = "success"
                data["code"] = 1
                data["line"] = line.get_geojson()
                return HttpResponse(simplejson.dumps(data), status=200,
                                    mimetype='application/json')
            else:
                return HttpResponse(status=400, content="No rights")
        else:
            return HttpResponse(status=400, content=form.errors)
    
    
def create_line(request):
    if request.POST:
        form = GeoLineTagForm(request.POST)
        
        if form.is_valid():
            line = form.save(request.user)
            data = {}
            data["type"] = "success"
            data["code"] = 1
            data["line"] = line.get_geojson()
            return HttpResponse(simplejson.dumps(data), status=200,
                                mimetype='application/json')
        else:
            return HttpResponse(status=400, content=form.errors)
    
    
    
    