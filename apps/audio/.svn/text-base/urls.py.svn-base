from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # all audio or latest audio
    url(r'^$', 'audio.views.index', name="audio"),

    # a audio details
    url(r'^details/(?P<id>\d+)/$', 'audio.views.details', name="audio_details"),

    # upload audio
    url(r'^audio-upload/$', 'audio.views.upload', name="audio_upload"),

    url(r'^flash_upload/$', 'audio.views.flash_upload', name="flash_audio_upload"),

    # your audio
    #url(r'^youraudio/$', 'audio.views.youraudio', name='audio_yours'),

    # a members audio
    #url(r'^member/(?P<username>[\w\.-]+)/$', 'audio.views.memberaudio', name='audio_member'),

    #destory audio
    url(r'^destroy/(\d+)/$', 'audio.views.destroy', name='audio_destroy'),

    #edit audio
    url(r'^edit/(\d+)/$', 'audio.views.edit', name='audio_edit'),
)
