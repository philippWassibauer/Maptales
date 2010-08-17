from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from account.forms import SignupForm
from voting.views import vote_on_object
from story.models import Story

import os.path



story_vote_dict = {
    'model': Story,
    'template_object_name': 'story',
    'allow_xmlhttprequest': 'true',
}


from blog.feeds import BlogFeedAll, BlogFeedUser
blogs_feed_dict = {"feed_dict": {
    'all': BlogFeedAll,
    'only': BlogFeedUser,
}}

from bookmarks.feeds import BookmarkFeed
bookmarks_feed_dict = {"feed_dict": { '': BookmarkFeed }}

admin.autodiscover()

#for now neeeded for the application -- dont remove
js_info_dict = {
    'packages': ( 'myapp.myproject',),
}

handler500 = 'maptales_app.views.handler500'


urlpatterns = patterns('',
    (r'^', include('maptales_app.urls')),               
    (r'^account/', include('account.urls')),
    
    url(r'^story-vote/(?P<object_id>[0-9]+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, story_vote_dict, name="tip-voting"),

    url(r'^socialregister/facebook/login/$', 'socialregistration.views.facebook_login', {"extra_context":{"signup_form":SignupForm()}}, name='facebook_login'),
    url(r'^android-app/', direct_to_template, {'template': 'android.html'}, name="androidapp"),
    url(r'^iphone-app/', direct_to_template, {'template': 'iphone.html'}, name="iphoneapp"),
    url(r'^learn-more/', direct_to_template, {'template': 'learnmore.html'}, name="learnmore"),
    #(r'^xd_receiver.htm', direct_to_template, {"template": "xd_receiver.html"}),

    (r'^profiles/', include('profiles.urls')),
    (r'^blog/', include('blog.urls')),
    (r'^featured/', include('featured.urls')),
    (r'^tags/', include('tag_app.urls')),
    (r'^invitations/', include('friends_app.urls')),
    (r'^notices/', include('notification.urls')),
    (r'^messages/', include('messages.urls')),
    (r'^announcements/', include('announcements.urls')),
    (r'^comments/', include('threadedcomments.urls')),
    (r'^robots.txt$', include('robots.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^admin/', include(admin.site.urls)), 
    (r'^photos/', include('photos.urls')),
    (r'^audio/', include('audio.urls')),
    (r'^avatar/', include('avatar.urls')),
    (r'^geo/', include('geo.urls')),
    (r'^activity/', include('activity_stream.urls')),
    (r'^flag/', include('flag.urls')),
    (r'^categories/', include('categories.urls')),   
    (r'^video/', include('video.urls')),
    (r'^story/', include('story.urls')),
    (r'^facebook/', include('facebook_maptales.urls')),
    (r'^feeds/posts/(.*)/$', 'django.contrib.syndication.views.feed', blogs_feed_dict),
    (r'^feeds/bookmarks/(.*)/?$', 'django.contrib.syndication.views.feed', bookmarks_feed_dict),
    #(r'^tinymce/', include('tinymce.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^contact', include('contact_form.urls')),
    (r'^mobile-clients/', include('mobile_clients.urls')),
    #for now neeeded for the application -- dont remove
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    
    (r'^badges', include('brabeion.urls')),
    
    #url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': CMSSitemap}}),
    
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    
    (r'^socialregister/', include('socialregistration.urls')),
    #url(r'natural_earth^', include('natural_earth.urls')),

    (r'^authsub/', include('authsub.urls')),
    (r'^bbauth/', include('bbauth.urls')),
    
    url(r'^ajax/hit/$', "hitcount.views.update_hit_count_ajax",name='hitcount_update_ajax'), # keep this name the same
    
    
    url(r'^', include('cms.urls')),
    url(r'^u/([-\w]+)', "activity_stream.views.activity_stream", name='profile_activity'),
)


## @@@ for now, we'll use friends_app to glue this stuff together

from photos.models import Image

friends_photos_kwargs = {
    "template_name": "photos/friends_photos.html",
    "friends_objects_function": lambda users: Image.objects.filter(member__in=users),
}

from blog.models import Post

friends_blogs_kwargs = {
    "template_name": "blog/friends_posts.html",
    "friends_objects_function": lambda users: Post.objects.filter(author__in=users),
}

from bookmarks.models import Bookmark

friends_bookmarks_kwargs = {
    "template_name": "bookmarks/friends_bookmarks.html",
    "friends_objects_function": lambda users: Bookmark.objects.filter(saved_instances__user__in=users),
    "extra_context": {
        "user_bookmarks": lambda request: Bookmark.objects.filter(saved_instances__user=request.user),
    },
}

urlpatterns += patterns('',
    url('^photos/friends_photos/$', 'friends_app.views.friends_objects', kwargs=friends_photos_kwargs, name="friends_photos"),
    url('^blog/friends_blogs/$', 'friends_app.views.friends_objects', kwargs=friends_blogs_kwargs, name="friends_blogs"),
    url('^bookmarks/friends_bookmarks/$', 'friends_app.views.friends_objects', kwargs=friends_bookmarks_kwargs, name="friends_bookmarks"),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),
    )