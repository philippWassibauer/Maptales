from django.template import Library
from django.contrib.contenttypes.models import ContentType
from story.models import Story, StoryLineItemMedia
from native_tags.decorators import function, comparison, filter
from django.template.loader import render_to_string
from django.template import RequestContext


register = Library()


def show_storyline(story, template_name="storyline.html"):
    storyline = story.storyline.order_by("position").all()
    return render_to_string(template_name, {
        "story": story,
        "storyline": storyline,
    })
show_storyline = function(show_storyline)


def show_storyline_slider(story, select_callback=None, finished_callback=None, template_name="story/storyline_slider.html"):
    storyline = story.storyline.order_by("position").all()
    return render_to_string(template_name, {
        "story": story,
        "select_callback": select_callback,
        "finished_callback": finished_callback,
    })
show_storyline_slider = function(show_storyline_slider)


def put_story_on_map(story, editable, template_name="story/put_story_on_map.html"):
    return render_to_string(template_name, {
        "story": story,
        "editable": editable,
    })
put_story_on_map = function(put_story_on_map)


@register.inclusion_tag("story/big_pic_teaser.html")
def story_big_pic_teaser(story, editable):
    return {
        "story": story,
        "editable": editable,
    }
    

@register.inclusion_tag("story/big_teaser.html")
def story_big_teaser(story):
    return {
        "story": story,
    }


def story_post_form(request, story, post=None, template_name="story/post_form.html"):
    storyline = story.storyline.order_by("position").all()
    return render_to_string(template_name, {
        "story": story,
        "storyline": storyline,
        "post":  post,
    }, context_instance=RequestContext(request))
story_post_form = function(story_post_form)
    
@register.inclusion_tag("story/stories_containing.html")
def stories_containing(object):
    content_type = ContentType.objects.get_for_model(object)
    stories = Story.objects.filter(storyline__attachments__object_id=object.id, storyline__attachments__content_type=content_type)
    return {"stories": stories}
    
    
def stories_in_area(x1, y1, x2, y2):
    stories = Story.objects.search_in_area(x1, y1, x2, y2)
    return render_to_string("story/stories_containing.html", {
        "stories": stories,
    })
stories_in_area = function(stories_in_area)


def stories_nearby(x, y, filtered_story=None, offset=0, count=3):
    if not x or not y:
        return ""
    stories = Story.objects.nearby(x,y,filtered_story)
    return render_to_string("story/stories_nearby.html", {
        "stories": stories,
    })
stories_nearby = function(stories_nearby)


def story_embedded(story, width, height, style=None):
    from django.contrib.sites.models import Site
    return render_to_string("story/embedded_iframe.html", {
        "domain": Site.objects.get_current(),
        "story": story,
        "width": width,
        "height": height,
    })
story_embedded = function(story_embedded)

