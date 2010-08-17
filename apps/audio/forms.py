from django import forms
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

from audio.models import Audio


class AudioEditForm(forms.ModelForm):
    class Meta:
        model = Audio
        exclude = ('creator','comment', 'audio_file')

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(AudioEditForm, self).__init__(*args, **kwargs)

class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = Audio
        exclude = ('creator','comment')
        
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(AudioUploadForm, self).__init__(*args, **kwargs)

class AudioFlashUploadForm(forms.ModelForm):

    class Meta:
        model = Audio
        exclude = ('creator','comment','cover')

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(AudioFlashUploadForm, self).__init__(*args, **kwargs)
