from django.forms import ModelForm
from django.forms import Form
from django import forms
from video.models import Video
from oembed.models import ProviderRule
import re
from oembed.core import fetch
from django.conf import settings
from oembed.core import re_parts
import simplejson
from django.template.loader import render_to_string

class VideoForm(Form):
    title = forms.CharField(max_length=300)
    comment = forms.CharField(max_length=300, widget=forms.widgets.Textarea() )
    tags = forms.CharField(max_length=300)
    video = forms.FileField()

class VideoEditForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = ('thumbnail_url','import_url','was_uploaded','creator',
                   'ticket_id', 'original_file', 'external_id', 'is_viewable')

    def __init__(self, user=None, *args, **kwargs):
        self.creator = user
        super(VideoEditForm, self).__init__(*args, **kwargs)

class VideoStoryEditForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = ('title', 'thumbnail_url','import_url','was_uploaded','creator',
                   'ticket_id', 'original_file', 'external_id', 'is_viewable',
                   'safetylevel', 'from_html_code', 'html_code')


class VideoImportForm(Form):
    title = forms.CharField(max_length=300, required=False)
    url = forms.CharField(label="Import Url", max_length=300)

class StoryVideoForm(Form):
    title = forms.CharField(max_length=300, required=False)
    url = forms.CharField(label="Import Url", max_length=300)
    html_code = forms.CharField(max_length=300, required=False)
    
    def save(self, user):
        video = None
        rules = list(ProviderRule.objects.all())
        patterns = [re.compile(r.regex) for r in rules]
        self.full_clean()
        for i, part in re_parts(patterns, self.cleaned_data['url']):
            rule = rules[i]
            FORMAT = getattr(settings, "OEMBED_FORMAT", "json")
            url = u"%s?url=%s&maxwidth=%s&maxheight=%s&format=%s" % (
                rule.endpoint, part, 600, 400, FORMAT
            )

            resp = simplejson.loads(fetch(url))
            replacement = render_to_string('oembed/%s.html' % resp['type'], {'response': resp})

        # TODO: this should be in oembed, bit dont want to modify it now
        if(resp):
            if(resp.has_key('thumbnail_url')):
               thumbnail_url = resp['thumbnail_url']
            else:
               p = re.compile('v=([^&]+)')
               m = p.search(self.cleaned_data['url'])
               id = m.group()
               id = id.replace("v=","")
               thumbnail_url = "http://img.youtube.com/vi/"+id+"/1.jpg"
               #import pdb; pdb.set_trace()

                
            video = Video(creator= user,
                          import_url=self.cleaned_data['url'],
                          was_uploaded=False,
                          thumbnail_url=thumbnail_url,
                          title=self.cleaned_data['title'],
                         )
            video.save()
        return video
        
class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = ('thumbnail_url','import_url','was_uploaded','creator')

    def __init__(self, user=None, *args, **kwargs):
        self.creator = user
        super(VideoUploadForm, self).__init__(*args, **kwargs)
