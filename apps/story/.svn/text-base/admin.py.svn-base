from django.contrib import admin
from story.models import Story, StoryLineItem

admin.site.register(Story)


class StoryLineItemAdmin(admin.ModelAdmin):
    list_display        = ('story', 'position')
    list_filter         = ('story',)
    search_fields       = ('story',)

admin.site.register(StoryLineItem, StoryLineItemAdmin)

