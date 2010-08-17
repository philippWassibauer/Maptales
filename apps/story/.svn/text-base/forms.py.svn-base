from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from story.models import Story, StoryLineItem, StoryLineItemMedia
from widgets.widgets import DojoEditorWidget
from categories.forms import CategoryMultipleChoiceField
from categories.models import CategorizedItem
from blog.models import Post
from activity_stream.models import create_activity_item
from django.contrib.gis.geos import LineString, Point
from geo.models import GeoPointTag
from misc.utils import get_target_object
from photos.models import Image
from django.core.files.base import ContentFile
import os
import logging

class MobileStoryLineItemForm(forms.Form):
    text = forms.CharField(max_length=500, required=False)
    image = forms.ImageField(required=False)
    lat = forms.CharField(required=False)
    lng = forms.CharField(required=False)
    id = forms.IntegerField(required=False)
    timestamp = forms.DateTimeField(required=False)
    
    def save(self, user, story):
        
        logging.debug("Adding Post to Experience")
        if self.cleaned_data['id']:
            post = StoryLineItem.objects.get(pk=self.cleaned_data['id'])
            post.text = self.cleaned_data['text']
        else:
            post = StoryLineItem(text=self.cleaned_data['text'],
                                 creator=user,
                                 story=story)
        post.save()
        
        if self.cleaned_data['lng'] and self.cleaned_data['lat']:
            location = Point(float(self.cleaned_data['lng']),
                             float(self.cleaned_data['lat']))
            
            pointTag = GeoPointTag(content_object=post,
                                              location=location,
                                              creator=user)
            pointTag.save()
        
        # add medias
        if self.cleaned_data["image"]:
            logging.debug("Adding Post With Image")
            title = "IPhone - %s"%self.cleaned_data["timestamp"]
            image = Image(title=title)
            image.image.save(os.path.basename(story.title+"-"+title),
                             ContentFile(self.cleaned_data["image"].read()))
            image.save()
            storylineAttachment = StoryLineItemMedia(storylineitem=post,
                                                     content_object=image)
            storylineAttachment.save()
            logging.debug("Finished Saving Image")
        return post
    
    
class StoryLineItemForm(forms.Form):
    text = forms.CharField(max_length=500, required=False)
    medias = forms.CharField(required=False)
    lat = forms.CharField(required=False)
    lng = forms.CharField(required=False)
    id = forms.IntegerField(required=False)
    
    def save(self, user, story):
        if self.cleaned_data['id']:
            post = StoryLineItem.objects.get(pk=self.cleaned_data['id'])
            post.text = self.cleaned_data['text']
        else:
            post = StoryLineItem(text=self.cleaned_data['text'],
                                 creator=user,
                                 story=story)
        post.save()
        
        if self.cleaned_data['lng'] and self.cleaned_data['lat']:
            location = Point(float(self.cleaned_data['lng']),
                             float(self.cleaned_data['lat']))
            
            pointTag = GeoPointTag(content_object=post,
                                              location=location,
                                              creator=user)
            pointTag.save()
        
        # add medias
        if self.cleaned_data["medias"]:
            media_uids = self.cleaned_data["medias"].split(",")
            for media_uid in media_uids:
                media = get_target_object(media_uid.strip())
                storylineitem = StoryLineItemMedia(storylineitem=post,
                                   content_object=media)
                storylineitem.save()
        return post


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('author', 'creator', 'slug', 'creation_date', 'update_date',
                    'geometry_collection', 'mapmode', "from_location_name",  "to_location_name", "tracks" )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['categories'] = CategoryMultipleChoiceField(label=_("Which Categories?"), required=False)


    def save(self, user):
        story = super(StoryForm, self).save(commit=False)
        from django.template.defaultfilters import slugify
        story.slug = slugify(story.title)
        story.creator = user
        from misc.utils import make_unique
        story.slug = make_unique(story, lambda x: Story.objects.filter(slug__exact=x.slug).exclude(pk=story.pk).count() == 0)
        story.status = Story.STATUS_DRAFT
        story.save()

        for category in self.cleaned_data["categories"]:
            item = CategorizedItem.objects.create(object=story, category=category)

        if story.status == story.STATUS_PUBLIC:
            create_activity_item("created_story", user, story)
            
        return story
    
    
class StoryEditForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('description', 'privacy', 'mapmode')
        
    def __init__(self, *args, **kwargs):
        super(StoryEditForm, self).__init__(*args, **kwargs)
        initial = []
        if self.instance:
            categorized_items = self.instance.categories.all()
            initial = [categorized_item.category.id for categorized_item in categorized_items]
        self.fields['categories'] = CategoryMultipleChoiceField(label=_("Which Categories?"), required=False, initial=initial)

    def save(self, user):
        self.user = user
        
        if self.cleaned_data.get("title", False):
            self.instance.title = self.cleaned_data["title"]
            from django.template.defaultfilters import slugify
            self.instance.slug = slugify(self.cleaned_data["title"])
            from misc.utils import make_unique
            self.instance.slug = make_unique(self.instance, lambda x: Story.objects.filter(slug__exact=x.slug).exclude(pk=x.id).count() == 0)
        
        if self.cleaned_data.get("description", False):
            self.instance.description = self.cleaned_data["description"]
        
        if self.cleaned_data.get("status", False):
            self.instance.status = self.cleaned_data["status"]
            
        if self.cleaned_data.get("mapmode", False):
            self.instance.mapmode = self.cleaned_data["mapmode"]
            
        if self.cleaned_data.get("privacy", False):
            self.instance.privacy = self.cleaned_data["privacy"]
            
        self.instance.creator = user
        self.instance.save()
        
        content_type = ContentType.objects.get_for_model(self.instance)
        for category in self.cleaned_data["categories"]:
            item = CategorizedItem.objects.get_or_create(object_id=self.instance.id, content_type=content_type,  category=category)
        
        if self.instance.status != self.instance.STATUS_PUBLIC:
            create_activity_item("created_story", user, self.instance)
            
        return self.instance