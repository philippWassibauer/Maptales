import os, re
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from story.models import Story, StoryLineItem
from photos.models import Image
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from geo.utils import convert_gpx_file

import datetime

from maptales_app.utils import get_model_name

class ProfilesTest(TestCase):

    def test_placing(self):
        c = Client()
        c.login(username='admin', password='localhost')
        profile = User.objects.get(username="admin").get_profile()

        self.assertEquals(profile.location, None)

        url = reverse('update_location')
        resp = c.post(url, {"lat": 12.44,"lng":54.00})
        profile = User.objects.get(username="admin").get_profile()
        
        self.assertEquals(profile.location.x, 54.00)
        self.assertEquals(profile.location.y, 12.44)
        self.assertEquals(profile.get_num_of_location_updates(), 1)


        url = reverse('update_location')
        resp = c.post(url, {"lat": 32.44,"lng":14.00})
        profile = User.objects.get(username="admin").get_profile()
        
        self.assertEquals(profile.location.x, 14.00)
        self.assertEquals(profile.location.y, 32.44)
        self.assertEquals(profile.get_num_of_location_updates(), 2)
