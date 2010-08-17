from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse

upload_parameters = {"redirect_to_path":True}

urlpatterns = patterns('',
    url(r'^place/$',  'geo.views.place_item', name='place_item'),
    url(r'^upload-gpx/$',  'geo.views.upload_gpx', kwargs=upload_parameters, name='upload_gpx'),
    url(r'^upload-gpx-ajax/$',  'geo.views.upload_gpx', name='upload_gpx_ajax'),

    url(r'^your-paths/$',  'geo.views.your_paths', name='your_paths'),
    url(r'^edit-path/(?P<id>\d+)$',  'geo.views.edit_path', name='edit_path'),
    url(r'^delete-path/(?P<id>\d+)$',  'geo.views.delete_path', name='delete_path'),

    url(r'^view-path/(?P<id>\d+)$',  'geo.views.view_path', name='view_path'),

    url(r'^geocode/$',  'geo.views.geocode', name='geocode'),

    url(r'^browse/$',  'geo.views.browse', name='browse'),
    url(r'^browse-user/$',  'geo.views.browse', {"template_name":"geo/user_map.html"},name='browse_user'),
    
    url(r'^ajax-browse/$',  'geo.views.ajax_browse', name='ajax_browse_all'),
    
    url(r'^get-clusters/$',  'geo.views.get_clusters', name="get_clusters"),
    
    url(r'^tags-in-area/$',  'geo.views.get_tags_in_area', name="get_tags_in_area"),
    
    
    url(r'^users-in-area/$',  'geo.views.users_in_area', name="users_in_area"),
    
    
    url(r'^country/(?P<country_name>[\w\.-]+)/$',  'geo.views.country', name='geo_country_browse'),

    url(r'^find-users-near-me/$',  'geo.views.find_users_near_me', name='find_users_near_me'),
    
    url(r'^track-selector-list/(?P<username>[\w\.-]+)/$',  'geo.views.track_selector_list', name='track_selector_list'),

    url(r'^create-line/$',  'geo.views.create_line', name='geo_create_line'),
    url(r'^update-line/$',  'geo.views.update_line', name='geo_update_line'),
    
)
