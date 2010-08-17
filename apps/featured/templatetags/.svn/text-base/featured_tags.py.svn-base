from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template import Library, Node, TemplateSyntaxError
from django.template import Variable, resolve_variable
from django.template import loader

from featured.models import FeaturedItem

import datetime

register = Library()
def suggest_featureditem():
    return ('mytitle', 'mybody')

class FeaturedStatusNode(Node):
    def __init__(self, obj, user, suggested_title=None, suggested_body=None):
        self.obj = Variable(obj)
        self.user = Variable(user)
        self.real_user = user
        self.suggested_title, self.suggested_body = Variable(suggested_title), Variable(suggested_body)
 
    def render(self, context):
        context['content_object'] = self.obj.resolve(context)
        context['content_type'] = ContentType.objects.get_for_model(context['content_object'])
        context['is_featured'] = FeaturedItem.objects.filter(content_type=context['content_type'], 
                                            object_id=context['content_object'].id)
        
        context['title'] = self.suggested_title.resolve(context)
        context['body'] = self.suggested_body.resolve(context)
        return loader.render_to_string('status.html', context)


def do_featured_status(parser, token):
    """
    Returns a url to the featured application, where the given object will be marked as featured
    {% featured_add_url some_object some_object.suggested_title some_object.suggested_body %}
    """
    try:
        bits = token.split_contents()
        tagname = bits[0]
    except ValueError:
        tagname = token.contents.split()[0]
        raise TemplateSyntaxError('tag "%s" requires one or three arguments' % tagname)

    if len(bits) != 5:
        raise TemplateSyntaxError('tag "%s" requires four arguments' % tagname)

    suggested_title = None
    suggested_body = None

    content_object = bits[1]
    user = bits[2]
    
    # suggested title/body will be used, to create add_link, if object is not already featured
    suggested_title = bits[3]
    suggested_body = bits[4]
    return FeaturedStatusNode(content_object, user, suggested_title, suggested_body)
    
register.tag('featured_status', do_featured_status)

@register.inclusion_tag("featured_list.html")
def featured_box_side(class_type, count):
    projects = FeaturedItem.objects.filter(content_type=ContentType.objects.get(name=class_type)).order_by('?')[0:count]
    return {"featured_projects": projects,
            "class_type": class_type}
