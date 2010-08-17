from django import forms

from django.contrib.auth.models import User
from django.db.models import Q
from friends.models import *
from friends.importer import import_vcards

try:
    from notification import models as notification
except ImportError:
    notification = None

# @@@ move to django-friends when ready


class ImportVCardForm(forms.Form):
    
    vcard_file = forms.FileField(label="vCard File")
    
    def save(self, user):
        imported, total = import_vcards(self.cleaned_data["vcard_file"].content, user)
        return imported, total


class FriendSelectorForm(forms.Form):
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(FriendSelectorForm, self).__init__(*args, **kwargs)
        users_ids = []
        users_ids.extend(Friendship.objects.filter(from_user=user).values_list('to_user', flat=True))
        users_ids.extend(Friendship.objects.filter(to_user=user).values_list('from_user', flat=True))
        users = User.objects.filter(pk__in=users_ids)
        self.fields['friends'] = forms.ModelMultipleChoiceField(queryset=users)


