
from django.conf.urls.defaults import *
from django.contrib.contenttypes.models import ContentType
from story.models import Story

urlpatterns = patterns('',
    url(r'^create/$',  'story.views.create', name='story_create'),
    url(r'^edit/(?P<id>[0-9]+)/$',  'story.views.edit', name='story_edit'),
    url(r'^preview/(?P<id>[0-9]+)/$',  'story.views.preview', name='story_preview'),
    url(r'^publish/(?P<id>[0-9]+)/$',  'story.views.publish', name='story_publish'),
    url(r'^delete/(?P<id>[0-9]+)/$',  'story.views.delete', name='story_delete'),
    
    url(r'^mobile-post/$',  'story.views.mobile_post', name='mobile_post'),
    url(r'^mobile-add-track-to-story/(?P<id>[0-9]+)/$',  'story.views.mobile_add_track', name='mobile_add_track'),
    url(r'^mobile-add-post-to-storyline/(?P<id>[0-9]+)/$',  'story.views.mobile_add_post_to_story', name='mobile_add_post_to_story'),
    
    
    url(r'^view/(?P<slug>[\w\.-]+)/$',  'story.views.view', name='story_view'),
    url(r'^v/(?P<id>[0-9]+)/$',  'story.views.view_id', name='story_view_id'),
    
    url(r'^remove-storyline-attachment/(?P<id>[0-9]+)/$',  'story.views.remove_storyline_attachment', name='remove_storyline_attachment'),
    
    url(r'^embed/(?P<slug>[\w\.-]+)/$',  'story.views.view',
        {'template_name':'story/embedded.html'}, name='story_embedded'),
    
    url(r'^full/(?P<slug>[\w\.-]+)/$',  'story.views.view',
        {'template_name':'story/fullscreen.html'}, name='story_fullscreen'),
    
    url(r'^ajax-browse$',  'story.views.stories_in_area',
        name='ajax_browse_stories'),
    
    
    url(r'^storyline/(?P<id>[0-9]+)/$',  'story.views.storyline', name='story_storyline'),
    url(r'^reorder_storyline/(?P<id>[0-9]+)/$', 'story.views.reorder_storyline', name="reorder_storyline"),
    url(r'^ajax-upload-gpx/(?P<id>[0-9]+)/$',  'story.views.upload_gpx', name='ajax_gpx_upload'),
    url(r'^your_stories/$',  'story.views.your_stories', name='your_stories'),
    url(r'^user/(?P<username>[\w\.-]+)/$',  'story.views.user_stories', name='user_stories'),
    url(r'^set-main-image/(?P<id>[0-9]+)/(?P<photo_id>\d+)/$',  'story.views.set_main_image', name='story_set_main_image'),
    url(r'^select-main-image/(?P<id>[0-9]+)/$',  'story.views.select_main_image', name='select_main_image'),
    url(r'^story-line-item/(?P<id>[0-9]+)/$',  'story.views.story_line_item', name='story_line_item'),
    url(r'^add-to-storyline/(?P<id>[0-9]+)/$',  'story.views.add_to_storyline', name='add_to_storyline'),
    url(r'^remove-storyline/(?P<story_id>[0-9]+)/(?P<id>\d+)$',  'story.views.remove_from_storyline', name='remove_from_storyline'),
    url(r'^add-path-to-story/(?P<id>[0-9]+)/$',  'story.views.add_path_to_story', name='add_path_to_story'),
    url(r'^remove-path-from-story/(?P<id>[0-9]+)/$',  'story.views.remove_path_from_story', name='remove_path_from_story'),
    url(r'^edit-storylineitem/$',  'story.views.edit_storylineitem', name='edit_storylineitem'),
    url(r'^add-video-to-storyline/(?P<id>[0-9]+)/$',  'story.views.add_video_to_story', name='add_video_to_story'),
    url(r'^add-post-to-storyline/(?P<id>[0-9]+)/$',  'story.views.add_post_to_story', name='add_post_to_story'),
    url(r'^add-post/(?P<id>[0-9]+)/$',  'story.views.add_post_to_story_screen', name='add_post_to_story_screen'),
    url(r'^add-video/(?P<id>[0-9]+)/$',  'story.views.add_video_to_story_screen', name='add_video_to_story_screen'),
    url(r'^attachment-list/$',  'story.views.storylineitem_attachments', name='storylineitem_attachments'),
    
    url(r'^edit-title/(?P<id>[0-9]+)/$',  'story.views.edit_story_title', name='edit_story_title'),
    
)
