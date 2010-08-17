import os, re
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from story.models import Story, StoryLineItem, StoryImage
from photos.models import Image
from story.templatetags.story_tags import stories_containing

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

class StoryTest(TestCase):
    def setUp(self):
        self.file_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), "../../test_data")
    
    def test_stories_containing(self):
        story = Story.objects.create(title='To Do', slug="to-do", creator=User.objects.get(pk=1))
        photo = Image.objects.create(title="1", title_slug="1")
        photo.image.save(os.path.basename('phot.jpg'), ContentFile(open(self.file_path+'/photo.jpg', "r").read()))
        photo.save()
        content_type = ContentType.objects.get_for_model(photo)
        story.storyline.create(content_type=content_type, object_id=photo.id, content_object=photo)
        
        tag_result = stories_containing(photo)
        self.assertEquals(len(tag_result["stories"]), 1)
        self.assertEquals(tag_result["stories"][0].id, story.id)
        
        #stories_in_area = Story.objects.search_in_area(10, 10, 20, 20)
        #self.assertFalse(stories_in_area)
        
    def test_image(self):
        story = Story.objects.create(title='To Do', slug="to-do", creator=User.objects.get(pk=1))
        
        photo = Image.objects.create(title="1", title_slug="1")
        photo.image.save(os.path.basename('pho.jpg'), ContentFile(open(self.file_path+'/photo.jpg', "r").read()))
        photo.save()

        self.assertEquals(1,1)

        storyImage = StoryImage.objects.create(image=photo.image, story=story)

        self.assertTrue(story.storyimage)
        self.assertTrue(story.storyimage.image)

        photo.delete()
        
        self.assertTrue(story.storyimage)
        self.assertTrue(story.storyimage.image)

    def test_image_http(self):
        story = Story.objects.create(title='To Do', slug="to-do", creator=User.objects.get(pk=1))

        photo = Image.objects.create(title="1", title_slug="1")
        photo.image.save(os.path.basename('p.jpg'), ContentFile(open(self.file_path+'/photo.jpg', "r").read()))
        photo.save()

        c = Client()
        c.login(username='admin', password='localhost')
        url = reverse('story_set_main_image', args=[story.slug, photo.id])

        resp = c.get(url, {"ll":"ll"})

        story2 = Story.objects.get(pk=story.id)

        self.assertTrue(story2.storyimage)
        self.assertTrue(story2.storyimage.image)



    def test_storyline(self):
        story = Story.objects.create(title='To Do', slug="to-do", creator=User.objects.get(pk=1))
        self.assertTrue(story)
        photo = Image.objects.create(title="1", title_slug="1")
        photo1 = Image.objects.create(title="2", title_slug="2")
        photo2 = Image.objects.create(title="3", title_slug="3")
        self.assertTrue(photo)
        content_type = ContentType.objects.get_for_model(story)
        story.storyline.create(content_type=content_type, object_id=photo.id, content_object=photo)
        story.storyline.create(content_type=content_type, object_id=photo1.id, content_object=photo1)
        story.storyline.create(content_type=content_type, object_id=photo2.id, content_object=photo2)
        self.assertEqual(story.storyline.count(), 3)
        self.assertEqual(story.storyline.all().order_by("position")[0].content_object, photo)
        self.assertEqual(story.storyline.all().order_by("position")[2].content_object, photo2)
        self.assertEqual(story.storyline.all().order_by("position")[0].position, 0)
        self.assertEqual(story.storyline.all().order_by("position")[2].position, 2)

        last_item = story.storyline.all().order_by("position")[2]
        last_item.position = 0
        last_item.save()

        self.assertEqual(story.storyline.all().order_by("position")[0].content_object, photo2)
        self.assertEqual(story.storyline.all().order_by("position")[1].content_object, photo)

        self.assertEqual(last_item.position, 0)

        url = reverse('reorder_storyline', args=[story.id])

        self.assertTrue(url)
        c = Client()
        c.login(username='admin', password='localhost')
        
        resp = c.post(url, {"newPosition": 2,"oldPosition": 0})
        self.assertEquals(resp.status_code, 200)
        self.assertTrue(resp.content)
        
        self.assertEqual(story.storyline.all().order_by("position")[0].content_object, photo)
        self.assertEqual(story.storyline.all().order_by("position")[2].content_object, photo2)

        #missing parameter
        resp = c.post(url, {"newPosition": 2})
        self.assertEquals(resp.status_code, 400)

        #out of range
        resp = c.post(url, {"newPosition": 3,"oldPosition": 0})
        self.assertEquals(resp.status_code, 400)