from django import forms
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

from photos.models import Image
from widgets.widgets import GoogleMapsWidget
from geo.forms import LocationInputField


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ('member','photoset','title_slug','effect','crop_from', 'is_public', 'location_name')
    
    def clean_image(self):
        if '#' in self.cleaned_data['image'].name:
            raise forms.ValidationError(
                _("Image filename contains an invalid character: '#'. Please remove the character and try again."))
        #re.sub("[^a-zA-Z 0-9.]+", "", "")

        return self.cleaned_data['image']

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(PhotoUploadForm, self).__init__(*args, **kwargs)
        self.fields["location"] = LocationInputField()


class PhotoFlashUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ('safetylevel', 'title', 'member','photoset','title_slug','effect','crop_from', 'is_public')

    def clean_image(self):
        if '#' in self.cleaned_data['image'].name:
            raise forms.ValidationError(
                _("Image filename contains an invalid character: '#'. Please remove the character and try again."))
        return self.cleaned_data['image']

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(PhotoFlashUploadForm, self).__init__(*args, **kwargs)


class PhotoEditForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ('member','photoset','title_slug','effect','crop_from','image', 'is_public', 'location_name')
        
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(PhotoEditForm, self).__init__(*args, **kwargs)
        self.fields["location"] = LocationInputField()


class PhotoStoryEditForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ('title', 'member','photoset','title_slug','effect','crop_from','image', 'is_public', 'location_name', "location", "safetylevel")

