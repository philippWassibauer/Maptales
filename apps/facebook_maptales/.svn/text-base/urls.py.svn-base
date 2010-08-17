from django.conf.urls.defaults import *

# Hack to get the project name
import django.views.generic.simple
project = __name__.split('.')[0]

# You'd want to change this to wherever your app lives
urlpatterns = patterns('',
    # Some functionality - users can post text to their homepage
    (r'^canvas/post/', 'facebook_maptales.views.post'),

    # For the mock AJAX functionality
    (r'^canvas/ajax/', 'facebook_maptales.views.ajax'),

    # This is the canvas callback, i.e. what will be seen
    # when you visit http://apps.facebook.com/<appname>.
    (r'^canvas/', 'facebook_maptales.views.canvas'),

    # Extra callbacks can be set in the Facebook app settings
    # page. For example, post_add will be called when a user
    # has added the application.
    (r'^post_add/', 'facebook_maptales.views.post_add'),

    url(r'^connect/', 'facebook_maptales.views.connect'),

    url(r'^start-story/', 'story.views.create', kwargs={"template_name":"facebook/start_story.html"}, name="fb_start_story" ),
)
