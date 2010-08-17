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
from geo.models import MGPXTrack, GeoAbstractModel
import datetime
from tagging.models import Tag

from maptales_app.utils import get_model_name
from django.core import management
from os.path import abspath

class GeoTest(TestCase):
    #fixtures = ['mine']

    def setUp(self):
        self.file_path = os.path.join(
                  os.path.join(os.path.dirname(__file__), "../../../test_data"))
                                      
    
    def create_gpx_track(self, filename):
        file = open(self.file_path+filename)
        track = MGPXTrack(creator=User.objects.get(username="admin"),
                          gpx_file=ContentFile(file.read()))
        file = open(self.file_path+'/Rothaarsteig_1.gpx')
        track = convert_gpx_file(file, track)
        file.close()
        return track
        
    def test_placing(self):
        photo = Image.objects.create(title="1", title_slug="1")
        photo.image.save(os.path.basename('ph.jpg'),
                         ContentFile(open(self.file_path+'/photo.jpg', "r")
                                                                    .read()))
        photo.save()
        
        self.assertTrue(photo)
        content_type = ContentType.objects.get_for_model(photo)
    
        self.assertFalse(photo.has_location())
        url = reverse('place_item')
        self.assertTrue(url)
        
        c = Client()
        
        #test without login
        resp = c.post(url, {"content_type": get_model_name(photo),
                            "content_object_id": photo.id,
                            "lat":"12.090", "lng":"13.99"})
        self.assertEquals(resp.status_code, 302)
        
        c.login(username='admin', password='localhost')
        
        #test without lat
        resp = c.post(url, {"content_type": get_model_name(photo),
                            "content_object_id": photo.id,
                            "lng":"13.99"})
        self.assertEquals(resp.status_code, 400)
        
        #test without content_type
        resp = c.post(url, {"content_object_id": photo.id,
                            "lat":"12.090", "lng":"13.99"})
        self.assertEquals(resp.status_code, 400)
        
        #test outside of valid area
        resp = c.post(url, {"content_object_id": photo.id,
                            "lat":"199.090", "lng":"13.99"})
        self.assertEquals(resp.status_code, 400)
        
        #test correct post
        resp = c.post(url, {"content_type": get_model_name(photo),
                            "content_object_id": photo.id,
                            "lat":"12.090", "lng":"13.99"})
        
        self.assertEquals(resp.status_code, 200)
        self.assertTrue(resp.content)

        # missing parameter
        self.assertEquals(Image.objects.get(pk=photo.id).location.get_x(),
                                                                        13.99)
        self.assertEquals(Image.objects.get(pk=photo.id).location.get_y(),
                                                                        12.090)
        
        # test searching for it
        from geo.models import GeoPointTag
        self.assertEquals(1,
                          len(GeoPointTag.objects.search_in_area(10,10,14,13)))
        self.assertEquals(0,
                          len(GeoPointTag.objects.search_in_area(10,10,12,12)))
        
        # test editing the 
        resp = c.post(url, {"content_type": get_model_name(photo),
                            "content_object_id": photo.id,
                            "lat":"24.090", "lng":"26.99"})
        
        self.assertEquals(resp.status_code, 200)
        self.assertTrue(photo.has_location())
        self.assertEquals(Image.objects.get(pk=photo.id).location.get_x(),
                                                                        26.99)
        self.assertEquals(Image.objects.get(pk=photo.id).location.get_y(),
                                                                        24.090)
        
        self.assertEquals(1,
                          len(GeoPointTag.objects.search_in_area(20,20,30,30)))
        
        photo.delete()
        
        self.assertEquals(0,
                          len(GeoPointTag.objects.search_in_area(10,10,14,13)))


    def test_gpx_convert(self):
        track = self.create_gpx_track("/Rothaarsteig_1.gpx")
        self.assertTrue(track)
        self.assertEqual(track.title, "ACTIVE LOG 003")
        self.assertEqual(round(track.distance, 5), 13.23896)
        self.assertEqual(track.start_time,datetime.datetime(2009, 9, 26, 2, 26))
        self.assertEqual(track.end_time, datetime.datetime(2009, 9, 26, 11, 12))
        self.assertEqual(track.segments.count(), 1)
        self.assertEqual(track.segments.all()[0].track.num_points, 400)
        self.assertEqual(track.segments.all()[0].track.array[0][0],
                                                            19.968699999999998)


    def test_gpx_upload_and_search(self):
        file = open(self.file_path+'/Rothaarsteig_1.gpx')
        c = Client()
        c.login(username='admin', password='localhost')
        url = reverse('upload_gpx_ajax')
        resp = c.post(url, {"gpx_file": file,"safetylevel":"1"})
        self.assertEquals(resp.status_code, 200)
        self.assertTrue(resp.content)
        
        #test output
        from django.utils import simplejson
        obj = simplejson.loads( resp.content )

        self.assertTrue(obj)

        self.assertEquals(obj["type"], "geo.mgpx_track")
        self.assertEquals(len(obj["segments"]), 1)
        self.assertEquals(len(obj["segments"][0]["track"]["coordinates"]), 400)
        
        file.close()
        
        self.assertEquals(1, len(MGPXTrack.objects.search_in_area(10,10,50,50)))
        self.assertEquals(1, len(MGPXTrack.objects.search_in_area(10,10,20,50)))
        self.assertEquals(0, len(MGPXTrack.objects.search_in_area(10,10,15,50)))
        
        
    def test_getting_filtered_content_in_area(self):
        track = self.create_gpx_track("/Rothaarsteig_1.gpx")
        track.tags = "one two three"
        track.save()
        
        self.assertEqual("one two three", track.tags)
        
        # get all items tagged with boarding in area
        #GeoPointTag.objects.filter(location__contained=NECountry.objects.get(name__contains="Slovakia").mpoly)
        
        # get all paths with category or tag
        
        from categories.models import Category
        category = Category.objects.get(slug="biking")
        self.assertEquals(1, len(MGPXTrack.objects.search_in_area(10,10,50,50)))
        
        
        # get all lines with category or tag
        
    def test_get_item_templatetag(self):
        from geo.templatetags.geo_tags import items_in_area
        self.assertEquals("ddddddd", items_in_area())
        
    def test_clustering(self):
        
        generate_clusterable_items()
        from ebgeo.utils.clustering.shortcuts import cluster_all_geoitems
        clusters = cluster_all_geoitems(GeoAbstractModel.objects.\
                                                search_in_area(10,10,15,15), 0)
        self.assertEqual(1, len(clusters))
        clusters2 = cluster_all_geoitems(GeoAbstractModel.objects.\
                                                search_in_area(10,10,15,15), 12)
        self.assertEqual(3, len(clusters2))
        
    def test_get_placed_unplaced(self):
        pass
    
    def test_track_select_list(self):
        c = Client()
        url = reverse("track_selector_list", args=("admin",))
        resp = c.get(url)
        self.assertEqual(302, resp.status_code)
        c.login(username='admin', password='localhost')
        resp = c.get(url)
        self.assertEqual(200, resp.status_code)
        
    def test_get_track_list(self):
        c = Client()
        url = reverse("your_paths")
        resp = c.get(url)
        self.assertEqual(302, resp.status_code)
        c.login(username='admin', password='localhost')
        resp = c.get(url)
        self.assertEqual(200, resp.status_code)
    
    def test_get_tagcloud_of_area(self):
        track = self.create_gpx_track("/Rothaarsteig_1.gpx")
        track.tags = "one two three"
        track.save()
        generate_clusterable_items()
        
        from geo.utils import tag_usage_for_queryset
        
        tags = tag_usage_for_queryset(GeoAbstractModel.objects\
                                      .search_in_area(10,10,60,60))
        tags2 = tag_usage_for_queryset(GeoAbstractModel.objects\
                                      .search_in_area(10,10,60,60), True)
        
    
    def test_get_active_users_in_area(self):
        from geo.utils import get_active_users_in_area
        c = Client()
        c.login(username='admin', password='localhost')
        track = self.create_gpx_track("/Rothaarsteig_1.gpx")
        track.tags = "one two three"
        track.save()
        
        users = get_active_users_in_area(10, 10, 13, 13)
        self.assertEqual(0, len(users))
        
        from blog.models import Post
        post = Post.objects.create(title="1", slug="1sdfwere", body="sd",
                                    author=User.objects.get(pk=1))
        post2 = Post.objects.create(title="112", slug="1sdfwere11", body="23sd",
                                    author=User.objects.get(pk=1))
        post3 = Post.objects.create(title="112234", slug="1sdfwere12341", body="23sd234",
                                    author=User.objects.get(pk=2))
        url = reverse('place_item')
        resp = c.post(url, {"content_type": get_model_name(post),
                            "content_object_id": post.id,
                                "lat":"12.090", "lng":"12.99"})
        resp = c.post(url, {"content_type": get_model_name(post2),
                            "content_object_id": post2.id,
                            "lat":"12.000", "lng":"12.00"})
        c.login(username='normal_user', password='localhost')
        resp = c.post(url, {"content_type": get_model_name(post3),
                            "content_object_id": post3.id,
                            "lat":"12.000", "lng":"12.00"})
        
        users = get_active_users_in_area(10, 10, 50, 50)
        self.assertEqual(2, len(users))
        self.assertEqual(4, users[0]['counter'])
        self.assertEqual(1, users[1]['counter'])
        
        users = get_active_users_in_area(10, 10, 13, 13)
        self.assertEqual(2, len(users))
        self.assertEqual(2, users[0]['counter'])
        self.assertEqual(1, users[1]['counter'])
        
        track.delete()
    
    def test_get_tagcloud_of_area_with_filter(self):
        file = open(self.file_path+'/Rothaarsteig_1.gpx')
        c = Client()
        c.login(username='admin', password='localhost')
        url = reverse('upload_gpx_ajax')
        resp = c.post(url, {"gpx_file": file,
                            "tags":"one two three",
                            "safetylevel":"1"})

        tags = Tag.objects.usage_for_queryset(
                                  MGPXTrack.objects.search_in_area(10,10,50,50),
                                  counts=True)
        
        self.assertEquals(3, len(tags))
        self.assertEquals(1, tags[0].count)
        
    def test_adding_and_updating_line_to_story(self):
        c = Client()
        c.login(username='admin', password='localhost')
        url = reverse('geo_create_line')
        story = Story.objects.create(title='To Do', slug="to-do",
                                     creator=User.objects.get(pk=1))
        
        resp = c.post(url, {"points": "0 0, 1 1, 2 2, 3 3, 4 4",
                            "content_type":get_model_name(story),
                            "content_object_id":story.pk})
        
        self.assertEquals(resp.status_code, 200)
        
        self.assertTrue(resp.content)
        
        #test output
        from django.utils import simplejson
        obj = simplejson.loads( resp.content )
        line = simplejson.loads( obj["line"] )
        
        print resp.content
        
        self.assertTrue(obj)
        self.assertEquals(line["type"], "geo.geo_line_tag")
        self.assertEquals(len(line["line"]["coordinates"]), 5)
        self.assertEquals(line["line"]["coordinates"][0][0], 0)
        self.assertEquals(line["line"]["coordinates"][0][1], 0)
        self.assertEquals(line["line"]["coordinates"][1][0], 1)
        self.assertEquals(line["line"]["coordinates"][1][1], 1)
        self.assertEquals(len(story.lines), 1)
        
        url = reverse('geo_update_line', args=(line["id"],))
        resp = c.post(url, {"points": "1 1, 1 1, 2 2, 3 3, 0 0"})
        
        self.assertEquals(resp.status_code, 200)
        
        self.assertTrue(resp.content)
        
        obj = simplejson.loads( resp.content )
        line = simplejson.loads( obj["line"] )
        self.assertTrue(obj)
        self.assertEquals(line["type"], "geo.geo_line_tag")
        self.assertEquals(len(line["line"]["coordinates"]), 5)
        self.assertEquals(line["line"]["coordinates"][0][0], 1)
        self.assertEquals(line["line"]["coordinates"][0][1], 1)
        self.assertEquals(line["line"]["coordinates"][4][0], 0)
        self.assertEquals(line["line"]["coordinates"][4][1], 0)
        

cluster_points = [
    (12, 12),
    (12, 12),
    (12, 12),
    (12.902, 12.234),
    (13.902, 14.234),
]

def generate_clusterable_items():
    from blog.models import Post
    c = Client()
    c.login(username='admin', password='localhost')
    count = 0
    for point in cluster_points:
        post = Post.objects.create(title="1", slug="1sdfwere_%s"%count,
                                   body="sd", author=User.objects.get(pk=1))
   
        url = reverse('place_item')
        resp = c.post(url, {"content_type": get_model_name(post),
                            "content_object_id": post.id,
                            "tags": "one two three",
                                "lat":point[0], "lng":point[1]})
        count = count+1
    