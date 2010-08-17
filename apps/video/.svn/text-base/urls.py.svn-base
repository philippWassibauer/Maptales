from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^$',         'video.views.index', name='videos'),
    url(r'^(?P<id>\d+)/$',      'video.views.show', name='show_video'),
    url(r'^edit/(?P<id>\d+)', 'video.views.edit', name='video_edit'),
    url(r'^delete/(?P<id>\d+)', 'video.views.destroy', name='video_destroy'),
    url(r'^create/$',  'video.views.create', name='video_create'),
    url(r'^import/$',  'video.views.import_video', name="video_import"),
    url(r'^upload/$',  'video.views.upload_video', name="upload_video"),
    url(r'^vimeo-callback/$',  'video.views.vimeo_callback'),
    url(r'^preview/$', 'video.views.preview_import', name="video_preview"),
    url(r'^vimeo-save/(?P<ticketId>\w+)$', 'video.views.vimeo_save_video', name="vimeo_save_video"),
    url(r'^oembed-video-url/(?P<id>\d+)/$',      'video.views.oembed_video_url', name='oembed_video_url'),
    url(r'^your-videos/$',      'video.views.your_videos', name='your_videos'),
    
    url(r'^video-selector-list/(?P<username>\w+)/$', 'video.views.video_selector_list', name='video_selector_list'),
)
