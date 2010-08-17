from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from BeautifulSoup import BeautifulSoup, Comment
from django.contrib.gis.forms.fields import GeometryField
from django.contrib.gis.maps.google.gmap import GoogleMap
from django.conf import settings

import django.contrib.gis.maps.google.gmap
from django.contrib.gis.geos import fromstr, Point, LineString, LinearRing, Polygon

class DojoEditorWidget(forms.HiddenInput):
    def __init__(self, text, field_name, *args, **kwargs):
        self.field_name = field_name
        self.text = text;
        super(DojoEditorWidget, self).__init__(*args, **kwargs)
    class Media:
        css = {'all': ('dojo/dijit/themes/nihilo/nihilo.css', 'dojo/dijit/themes/nihilo/Editor.css')}

    def render(self, name, value, attrs=None):
        output_string = render_to_string("editor/editor.html", {
            'text': self.text,
            'field_name': self.field_name,
            'class': "nihilo",
            'plugins': "['fontSize', 'formatBlock','|', 'undo','redo','|','block', 'bold','italic','underline','strikethrough','|','insertOrderedList', \
                        'insertUnorderedList','indent','outdent','|','justifyLeft','justifyRight','justifyCenter',\
                        'justifyFull', '|','insertHorizontalRule', 'createLink', 'insertImage']",
        })
        return mark_safe(output_string)

    def clean(self, value):
        value = super(DojoEditorWidget, self).clean(value)
        soup = BeautifulSoup(value)
        for comment in soup.findAll(
            text=lambda text: isinstance(text, Comment)):
            comment.extract()
        for tag in soup.findAll(True):
            if tag.name not in self.valid_tags:
                tag.hidden = True
            tag.attrs = [(attr, val) for attr, val in tag.attrs
                         if attr in self.valid_attrs]
        return soup.renderContents().decode('utf8')


class GoogleMapsWidget(forms.HiddenInput):
    def __init__(self, template="maps/google_maps_field.html", *args, **kwargs):
        self.GMAP = GoogleMap()
        self.template = template
        super(GoogleMapsWidget, self).__init__(*args, **kwargs)

    class Media:
        js = ('jquery/jquery-ui-1.7.2.custom.min.js',)

    def render(self, name, value, attrs=None):
        if isinstance(value, basestring):
            try:
                value = fromstr(value.strip())
            except:
                value = None
                
        if value and not (value.get_x()==0 and value.get_y()==0):
            out_value = str(value.get_x())+", "+str(value.get_y())
        else:
            out_value = None

        output_string = render_to_string(self.template, {
            'field_name': name,
            'item_to_place': attrs.get("item_to_place"),
            'db_value': value,
            'value': out_value,
            'default_center': "13, 0",
            'zoom': 1,
            'GMAP': self.GMAP,
        })
        return mark_safe(output_string)

    def clean(self, value):
        return value.strip()


class AdvancedFileWidget(forms.FileInput):
    def __init__(self, attrs={}):
        super(AdvancedFileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append('%s <a target="_blank" href="%s">%s</a> <br /><label>%s</label> ' % \
                (_('Currently:'), value.url, value, _('Change:')))
        output.append(super(AdvancedFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
