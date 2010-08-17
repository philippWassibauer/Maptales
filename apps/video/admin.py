from django.contrib import admin
from video.models import VimeoToken, Video, VideoImage

admin.site.register(VimeoToken)
admin.site.register(Video)
admin.site.register(VideoImage)
