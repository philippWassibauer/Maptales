import os, re
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
import datetime
from blog.models import Post

from maptales_app.utils import get_model_name

class BlogTest(TestCase):


    def test_placing(self):
        post = Post.objects.create(title="1", slug="1sdfwere", body="sd",
                                    author=User.objects.get(pk=1))
        
        
        content_type = ContentType.objects.get_for_model(post)

        url = reverse('place_item')
        self.assertTrue(url)
        
        c = Client()
        c.login(username='admin', password='localhost')

        resp = c.post(url, {"content_type": get_model_name(post),
                            "content_object_id": post.id,
                            "lat":"12.090", "lng":"13.99"})
        
        self.assertEquals(resp.status_code, 200)
        self.assertTrue(resp.content)

        # missing parameter
        self.assertEquals(Post.objects.get(pk=post.id).location.get_x(), 13.99)
        self.assertEquals(Post.objects.get(pk=post.id).location.get_y(), 12.090)
        
        # test searching for it
        from geo.models import GeoPointTag
        self.assertEquals(1, len(GeoPointTag.objects.search_in_area(10,10,14,13)))
        self.assertEquals(0, len(GeoPointTag.objects.search_in_area(10,10,12,12)))

        post.delete()
        
        self.assertEquals(0, len(GeoPointTag.objects.search_in_area(10,10,14,13)))

