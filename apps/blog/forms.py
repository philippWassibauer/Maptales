from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from blog.models import Post, PostImage
from widgets.widgets import DojoEditorWidget
from widgets.widgets import GoogleMapsWidget
from geo.forms import LocationInputField
from tinymce.widgets import TinyMCE
from django.conf import settings

class BlogImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        exclude = ('crop_from', 'effect', 'post',)

class BlogForm(forms.ModelForm):
    location = LocationInputField()
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 50, 'rows': 10}))
        
    class Meta:
        model = Post
        exclude = ('author', 'creator_ip', 'created_at', 'updated_at', 'publish', 'markup', 'status',
                    'allow_comments', 'slug', 'tease', 'location_name' )
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(BlogForm, self).__init__(*args, **kwargs)

    def save(self, request):
        blog = super(BlogForm, self).save(commit=False)
        init_blog_post(blog, request)
        blog.save()
        return blog;
        

class StoryPostForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(mce_attrs={"theme":"simple",
                                                     "theme_advanced_resize_horizontal": True,
                                                     "theme_advanced_resizing": True}, attrs={ 'cols': 50, 'rows': 10}))
    class Meta: 
        model = Post
        exclude = ('title', 'author', 'creator_ip', 'created_at', 'updated_at', 'publish', 'markup', 'status',
                    'allow_comments', 'slug', 'tease', 'location_name', "location", "safetylevel" )
    
    def save(self, request):
        blog = super(StoryPostForm, self).save(commit=False)
        init_blog_post(blog, request)
        blog.save()
        return blog;
    

def init_blog_post(blog, request):
    blog.author = request.user
    from django.template.defaultfilters import slugify
    blog.slug = slugify(blog.title)

    from misc.utils import make_unique
    blog.slug = make_unique(blog, lambda x: Post.objects.filter(slug__exact=x.slug).exclude(id=x.id).count() == 0)
    
    if settings.BEHIND_PROXY:
        blog.creator_ip = request.META["HTTP_X_FORWARDED_FOR"]
    else:
        blog.creator_ip = request.META['REMOTE_ADDR']
