from django.conf.urls.defaults import *

urlpatterns = patterns('',    
    # all photos or latest photos
    url(r'^$', 'photos.views.photos', name="photos"),
    # a photos details
    url(r'^details/(?P<id>\d+)/$', 'photos.views.details', name="photo_details"),
    
    url(r'^photo-browse-view/(?P<id>\d+)/$', 'photos.views.details', {"template_name":"photos/photo_detail_browse.html"}, name="photo_details_browse"),
    
    url(r'^ajax-browse-images/$', 'geo.views.ajax_browse', {"template_name":"photos/photo_in_area.html", "content_type":"photos.image"}, name="ajax_browse_images"),
    
    # upload photos
    url(r'^upload/$', 'photos.views.upload', name="photo_upload"),

    url(r'^upload-embedded/$', 'photos.views.upload', name="photo_upload_embedded", kwargs={"template_name":"photos/upload_embedded.html"}),

    url(r'^flash_upload/$', 'photos.views.flash_upload', name="photo_flash_upload"),

    # your photos
    url(r'^yourphotos/$', 'photos.views.yourphotos', name='photos_yours'),
    # a members photos
    url(r'^user/(?P<username>[\w]+)/$', 'photos.views.memberphotos', name='photos_member'),
    #destory photo
    url(r'^destroy/(\d+)/$', 'photos.views.destroy', name='photo_destroy'),
    #edit photo
    url(r'^edit/(\d+)/$', 'photos.views.edit', name='photo_edit'),
    url(r'^rotate/(\d+)/$', 'photos.views.rotate', name='photo_rotate'),
    url(r'^ajax-rotate/(\d+)/$', 'photos.views.rotate', kwargs={"redirect":False}, name='photo_ajax_rotate'),
    
    url(r'^select-photos/(?P<username>[\w]+)/$', 'photos.views.photo_selector', name='photo_selector'),
    
    url(r'^select-photos-list/(?P<username>[\w]+)/$', 'photos.views.photo_selector_list', name='photo_selector_list'),
)