from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'featured.views.list', name='featured-list'),
    url(r'^add/(?P<content_type_id>\d+)/(?P<content_object_id>\d+)/$', 'featured.views.add_or_edit', name='featured-add'),
    url(r'^edit/(?P<content_type_id>\d+)/(?P<content_object_id>\d+)/$', 'featured.views.add_or_edit', name='featured-edit'),
    url(r'^remove/(?P<content_type_id>\d+)/(?P<content_object_id>\d+)/$', 'featured.views.remove', name='featured-remove'),
)
