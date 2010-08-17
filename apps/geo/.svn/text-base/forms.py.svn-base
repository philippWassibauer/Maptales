from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _, ugettext
from geo.utils import convert_gpx_file, convert_mobile_app_to_linestring
import tempfile
from activity_stream.models import create_activity_item
from widgets.widgets import GoogleMapsWidget
from categories.forms import CategoryChoiceField, CategoryMultipleChoiceField
from categories.models import CategorizedItem
from geo.models import MGPXTrack, MGPXTrackSegment,GeoLineTag
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
import simplejson as json
from datetime import datetime

class GPXEditForm(forms.ModelForm):
    class Meta:
        model = MGPXTrack
        fields = ("title", "description", "safetylevel", "tags")
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(GPXEditForm, self).__init__(*args, **kwargs)


class GPXSegmentEditForm(forms.ModelForm):
    class Meta:
        model = MGPXTrackSegment
        fields = ("title", "description", "safetylevel", "tags")

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(GPXSegmentEditForm, self).__init__(*args, **kwargs)


class GPXUploadForm(forms.ModelForm):
    
    class Meta:
        model = MGPXTrack
        fields = ("title", "description", "gpx_file")
    
    def __init__(self, user, data=None, files=None, request=None, *args, **kwargs):
        self.user = user
        super(GPXUploadForm, self).__init__(data=data, files=files, *args, **kwargs)
        
    def save(self, fail_silently=False):

        filePath = tempfile.mktemp(".gpx")
        tempTrack = open(filePath, 'w')

        for line in self.files["gpx_file"].readlines():
            tempTrack.write(line)
        tempTrack.close()
        tempTrack = open(filePath, 'r')
        
        track = super(GPXUploadForm, self).save(commit=False)
        track.creator = self.user
        track = convert_gpx_file(tempTrack, track)
        
        track.save()

        for segment in track.segments.all():
            segment.render_chart()
            
        tempTrack.close()        
        #for category in self.cleaned_data["categories"]:
        #    item = CategorizedItem.objects.create(object=track, category=category)
        
        #create_activity_item("geodata_uploaded", self.user, track)
        
        return track
    

class MobileClientGPSForm(forms.Form):
    jsonPoints = forms.CharField(required=False)
    def save(self, user, story):
        if(self.cleaned_data["jsonPoints"]):
            convertedPoints = json.loads(self.cleaned_data['jsonPoints'])
            if(len(convertedPoints) > 1):
                start_time = None
                end_time = None
                
                if (hasattr(convertedPoints[0],"timestamp")):
                    try:
                        start_time = datetime.strptime(convertedPoints[0]["timestamp"], "%Y-%m-%d %H:%M:%S")
                    except:
                        pass
                
                if(hasattr(convertedPoints[-1], "timestamp")):
                    try:
                        end_time = datetime.strptime(convertedPoints[-1]["timestamp"], "%Y-%m-%d %H:%M:%S")
                    except:
                        pass
                
                privacy = 1
                if (story.privacy):
                    privacy = story.privacy
                    
                gpxTrack = MGPXTrack(title="IPhone Tracking", description="",
                                    safetylevel=privacy,
                                    start_time=start_time,
                                    end_time=end_time,
                                    creator=user)
                gpxTrack.save()
                track = convert_mobile_app_to_linestring(convertedPoints)
                trackSegment = MGPXTrackSegment(title="IPhone Tracking",
                                                description="IPhone Tracking",
                                                content_object=story,
                                                raw_track=convertedPoints,
                                                creator=user,
                                                track=track,
                                                parent=gpxTrack,
                                                distance=track.length,
                                                start_time = start_time,
                                                end_time = end_time)
                gpxTrack.set_story_reference(story)
                gpxTrack.save()
                trackSegment.save()
                
                return gpxTrack
            else:
                return None
        else:
            return None
        
        
class GPXUploadForm(forms.ModelForm):
    class Meta:
        model = MGPXTrack
        fields = ("title", "description", "gpx_file")
    
    def __init__(self, user, data=None, files=None, request=None, *args, **kwargs):
        self.user = user
        super(GPXUploadForm, self).__init__(data=data, files=files, *args, **kwargs)
        
    def save(self, fail_silently=False):

        filePath = tempfile.mktemp(".gpx")
        tempTrack = open(filePath, 'w')

        for line in self.files["gpx_file"].readlines():
            tempTrack.write(line)
        tempTrack.close()
        tempTrack = open(filePath, 'r')
        
        track = super(GPXUploadForm, self).save(commit=False)
        track.creator = self.user
        track = convert_gpx_file(tempTrack, track)
        
        track.save()

        for segment in track.segments.all():
            segment.render_chart()
            
        tempTrack.close()        
        #for category in self.cleaned_data["categories"]:
        #    item = CategorizedItem.objects.create(object=track, category=category)
        
        #create_activity_item("geodata_uploaded", self.user, track)
        
        return track


class LocationInputField(forms.CharField):
    widget=GoogleMapsWidget
    def __init__(self, *args, **kwargs):
        super(LocationInputField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        return {"one": "one"}

    def clean(self, value):
        if value:
            return value  
        else:
            raise forms.ValidationError("This field is required.")


class LocationInputForm(forms.Form): 
    location = LocationInputField(label=_("location"), required=False,
                                  widget=GoogleMapsWidget(template='maps/google_maps_side_input.html'))
    

class GeoLineTagForm(forms.ModelForm):
    content_type = forms.CharField(required=True, label='content_type')
    points = forms.CharField(required=True, label='points')
    content_object_id = forms.IntegerField(required=True,
                                                   label='content_object_id')
    class Meta:
        model = GeoLineTag
        fields = ("title", "description", "content_object_id", "content_type")
    
    def clean_content_type(self):
        if not self.cleaned_data["content_type"]:
            raise forms.ValidationError(_("content_type has to be defined"))
            
        content_type = self.cleaned_data["content_type"]
        content_type_split = content_type.split(".")
        content_type = ContentType.objects.filter(app_label=content_type_split[0],
                                                  name=content_type_split[1])
        if content_type:
            return content_type[0]
        else:
            raise forms.ValidationError(_("content_type has to be defined"))
    
    def clean_content_object_id(self):
        if not self.cleaned_data["content_object_id"]:
            raise forms.ValidationError(_("content_object_id has to be defined"))
        return self.cleaned_data["content_object_id"]
        
    def clean_points(self):
        if not self.cleaned_data["points"]:
            raise forms.ValidationError(_("points has to be defined"))
        #TODO: regex here
        return self.cleaned_data["points"]
        
    def save(self, user, fail_silently=False):
        target_object = get_target_object(self.cleaned_data["content_type"], 
                                          self.cleaned_data["content_object_id"])
        linestring = "LINESTRING(%s)"%self.cleaned_data["points"]
        geolinetag = super(GeoLineTagForm, self).save(commit=False)
        geolinetag.content_type = self.cleaned_data["content_type"]
        geolinetag.object_id = target_object.pk
        geolinetag.content_object = target_object
        geolinetag.line = linestring
        geolinetag.creator=user
        geolinetag.save()
        return geolinetag


class GeoLineTagUpdateForm(forms.ModelForm):
    points = forms.CharField(required=True, label='points')
    class Meta:
        model = GeoLineTag
        fields = ("title", "description", "points")
        
    def clean_points(self):
        if not self.cleaned_data["points"]:
            raise forms.ValidationError(_("points has to be defined"))
        #TODO: regex here
        return self.cleaned_data["points"]
        
    def save(self, user, fail_silently=False):
        linestring = "LINESTRING(%s)"%self.cleaned_data["points"]
        geolinetag = super(GeoLineTagUpdateForm, self).save(commit=False)
        geolinetag.line = linestring
        geolinetag.save()
        return geolinetag
    
    
def get_target_object(content_type, content_object_id):
    target_object = content_type.get_object_for_this_type (pk=content_object_id)
    return target_object