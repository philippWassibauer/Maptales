from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.files.base import ContentFile
from django.db import models

from photologue.models import ImageModel

class TestBlogPost(models.Model):
    title           = models.CharField(max_length=300)
    body            = models.TextField()

class FeaturedItemManager(models.Manager):
    def content_types_of_featured_items(self, user):
        content_type_ids = FeaturedItem.objects.all().values_list('content_type', flat=True).order_by('content_type').distinct()
        return ContentType.objects.in_bulk(list(content_type_ids)).values()
    
    def users_of_featured_item(self, featured_item):
        content_type = ContentType.objects.get_for_model(featured_item)

        featured_items = FeaturedItem.objects.filter(content_type__pk=content_type.id, object_id=featured_item.id)
        user_ids = featured_items.values_list('user', flat=True)
        return User.objects.in_bulk(list(user_ids)).values()

class FeaturedImage(ImageModel):
    featured_item = models.OneToOneField('FeaturedItem', primary_key=True) 
    
class FeaturedItem(models.Model):
    title           = models.CharField(max_length=300)
    body            = models.TextField()
    
    # image
    image           = models.ImageField(upload_to='featured', blank=True, null=True)

    # custom manager
    objects         = FeaturedItemManager()
    
    # bind featured items to a specific user
    user            = models.ForeignKey(User)
    
    # Contenttypes Framework
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    content_object  = generic.GenericForeignKey()

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs) # Call the "real" save() method.
        if self.image:
            self.featuredimage = FeaturedImage()
            self.featuredimage.image = self.image
            self.featuredimage.featured_item = self
            self.featuredimage.save()
        
    def __unicode__(self):
        return self.title
