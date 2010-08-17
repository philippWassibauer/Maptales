from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'friends_app.views.friends', name='invitations'),
    url(r'^contacts/$', 'friends_app.views.contacts',  name='invitations_contacts'),
    url(r'^accept/(\w+)/$', 'friends_app.views.accept_join', name='friends_accept_join'),
    url(r'^request/(\w+)/$', 'friends_app.views.request_friendship', name='request_friendship'),
    url(r'^accept-friendship/(\w+)/$', 'friends_app.views.accept_friendship', name='accept_friendship'),
)
