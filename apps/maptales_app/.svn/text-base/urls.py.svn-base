from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^$',         'maptales_app.views.index', name='home'),
    url(r'^v2/$',         'maptales_app.views.index', name='home_v2'),
    url(r'^private-beta/$',         'maptales_app.views.private_beta_email', name='private_beta_email'),
    url(r'^search$',         'maptales_app.views.search', name='search'),
    url(r'^what_next$',  'maptales_app.views.index', name='what_next'),
    url(r'^iphone$',  'maptales_app.views.iphone', name='iphone'),
    url(r'^global-activity',  'maptales_app.views.global_activity', name='global_activity'),
    url(r'^switch-users', 'maptales_app.views.switch_user', name="switch_user"),
    url(r'^passphrase_check', 'maptales_app.views.passphrase_check', name='passphrase_check'),
    url(r'^mobile_login/$',  'maptales_app.views.mobile_login', name='mobile_login'),
    url(r'^mobile_signup/$',  'maptales_app.views.mobile_signup', name='mobile_signup'),
)
