from django.conf import settings
from django import forms
from django.contrib.gis.geos import LineString, Point
from profiles.models import Profile
from activity_stream.models import create_activity_item

try:
    from notification import models as notification
except ImportError:
    notification = None

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'blogrss', 'timezone', 'language',
            'twitter_user', 'twitter_password', 'location', 'path')



class LocationUpdateForm(forms.Form):

    lat = forms.FloatField()
    lng = forms.FloatField()
    altitude = forms.FloatField(required=False)
    source = forms.CharField(required=False)

    user = None

    def save(self, user):
        if self.is_valid():
            profile = user.get_profile()
            lng = self.cleaned_data["lng"]
            lat = self.cleaned_data["lat"]
            profile.location = Point(lng,lat)
            profile.save()

            if profile.path:
                profile.path.append([lng, lat])
                profile.save()
            else:
                array = [ [lng, lat], [ lng, lat ] ]
                profile.path = LineString(array)
                profile.save()

            create_activity_item("user_location_update", user, user)   
        return False