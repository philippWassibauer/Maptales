from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

profile_edit_kwargs = { 'template_name': 'profiles/profile_edit.html' }

urlpatterns = patterns('',
    url(r'^username_autocomplete/$', 'profiles.views.username_autocomplete', name='profile_username_autocomplete'),
    url(r'^$', 'profiles.views.profiles', name='profile_list'),
    url(r'^(?P<username>[\w]+)/$', 'profiles.views.profile', name='profile_detail'),
    url(r'^(?P<username>[\w]+)/edit/$', 'profiles.views.profile', kwargs=profile_edit_kwargs, name='profile_edit' ),
    url(r'^(?P<username>[\w]+)/friends$', 'profiles.views.friends', name='profile_friends'),
    url(r'^friend-request/(?P<username>[\w]+)/$', 'profiles.views.friend_request', name='friend_request'),
    url(r'^update-location/$', 'profiles.views.update_location', name='update_location'),
    url(r'^change-email/$', 'profiles.views.change_email', name='change_email'),
    url(r'^profile-privacy/$', 'profiles.views.profile_privacy', name='profile_privacy'),
    url(r'^profile-notification/$', 'profiles.views.profile_notification',  name="profile_notification"),

)
