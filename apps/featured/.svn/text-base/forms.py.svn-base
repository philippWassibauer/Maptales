from featured.models import *
from django.forms import ModelForm, CharField
from django.forms.widgets import HiddenInput

class FeaturedItemForm(ModelForm):
    class Meta:
        model = FeaturedItem
        exclude = ('content_type', 'object_id', 'user',)