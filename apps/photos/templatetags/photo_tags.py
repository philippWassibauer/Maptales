import re
from django import template
from photos.models import Image
#from photologue.utils import EXIF
register = template.Library()
from misc.utils import safetylevel_filter
from native_tags.decorators import function, comparison, filter
from django.template import RequestContext
from django.template.loader import render_to_string

def add_photos_dialog(request, container_id, callback_function, content_object=None, template_name="photos/photo_add_dialog.html"):
    return render_to_string(template_name, {
        "callback_function": callback_function,
        "container_id": container_id,
    }, context_instance=RequestContext(request))
add_photos_dialog = function(add_photos_dialog)

@register.tag(name="print_exif")
def do_print_exif(parser, token):
    try:
        tag_name, exif = token.contents.split()
    except ValueError:
        msg = '%r tag requires a single argument' % token.contents[0]
        raise template.TemplateSyntaxError(msg)

    exif = parser.compile_filter(exif)
    return PrintExifNode(exif)

class PrintExifNode(template.Node):

    def __init__(self, exif):

        self.exif = exif

    def render(self, context):
        try:
            exif = unicode(self.exif.resolve(context, True))
        except template.VariableDoesNotExist:
            exif = u''

        EXPR =  "'(?P<key>[^:]*)'\:(?P<value>[^,]*),"
        expr = re.compile(EXPR)
        msg  = "<table>"
        for i in expr.findall(exif):
            msg += "<tr><td>%s</td><td>%s</td></tr>" % (i[0],i[1])

        msg += "</table>"

        return u'<div id="exif">%s</div>' % (msg)



def user_photo_stream_navigator(photo, user, logged_in_user):
    previous = None
    next = None
    #TODO: Add proper filter, is_public is not used at the moment
    try:
        #previous = safetylevel_filter(Image.objects.filter(is_public=True, date_added__lt=photo.date_added, member=user), "member", logged_in_user).order_by("-date_added")[0:1][0]
        previous = Image.objects.filter(is_public=True, date_added__gt=photo.date_added, member=user).order_by("date_added")[0:2]
    except:
        pass

    try:
        #next = safetylevel_filter(Image.objects.filter(is_public=True, date_added__gt=photo.date_added, member=user), "member", logged_in_user).order_by("date_added")[0:1][0]
        next = Image.objects.filter(is_public=True, date_added__lt=photo.date_added, member=user).order_by("-date_added")[0:2]
    except:
        pass
    
    index = Image.objects.filter(is_public=True, date_added__gt=photo.date_added, member=user).count()
    total = Image.objects.filter(is_public=True, member=user).count()

    return {"previous_items": previous,
            "next_items": next,
            "current": photo,
            "stream_user": user,
            "index": index,
            "total": total}
    
register.inclusion_tag("user_stream_navigator.html")(user_photo_stream_navigator)

def main_photo_stream_navigator(photo, logged_in_user):
    previous = None
    next = None

    try:
        previous = safetylevel_filter(Image.objects.filter(is_public=True, date_added__lt=photo.date_added), "member", logged_in_user).order_by("-date_added")[0:1][0]
    except:
        pass

    try:
        next = safetylevel_filter(Image.objects.filter(is_public=True, date_added__gt=photo.date_added), "member", logged_in_user).order_by("date_added")[0:1][0]
    except:
        pass

    return {"previous": previous,
            "next": next,
            "current": photo}
register.inclusion_tag("main_stream_navigator.html")(main_photo_stream_navigator)


