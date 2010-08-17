from django.template import Library
from native_tags.decorators import function, comparison, filter
from django.template import RequestContext
from django.template.loader import render_to_string
from video.models import Video
from video.forms import VideoForm
register = Library()

@register.inclusion_tag("video_teaser.html")
def show_video_teaser(video):
    return {"video": video}

@register.inclusion_tag("video_content.html")
def show_video_content(video):
    return {"video": video}
    

def add_video_dialog(request, container_id, callback_function=None, content_object=None, template_name="video/add_video_dialog.html"):
    return render_to_string(template_name, {
        "callback_function": callback_function,
        "container_id": container_id,
        "video_form": VideoForm(),
    }, context_instance=RequestContext(request))
add_video_dialog = function(add_video_dialog)


def video_selector_list(request, callback_function=None, template_name="video/video_selector_list.html"):
    user = request.user
    videos = Video.objects.filter(creator=user).order_by("-date_added")
    return render_to_string(template_name, {
        "viewed_user": user,
        "videos": videos,
        "callback_function": callback_function,
    }, context_instance=RequestContext(request))
video_selector_list = function(video_selector_list)