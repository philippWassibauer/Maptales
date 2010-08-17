from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db import models

from mailer import send_mail, mail_admins
from story.forms import StoryForm, StoryEditForm, MobileStoryLineItemForm
from story.models import Story, StoryImage, StoryLineItem

from avatar.templatetags.avatar_tags import avatar
from django.forms.models import   ModelMultipleChoiceField
from django.contrib.auth.decorators import login_required
from geo.forms import GPXUploadForm, MobileClientGPSForm
from photos.models import Image
import os
from django.core.files.base import ContentFile
from activity_stream.models import create_activity_item
from django.contrib.contenttypes.models import ContentType

from blog.forms import StoryPostForm
from video.forms import StoryVideoForm
from geo.models import MGPXTrack
from forms import StoryLineItemForm
from django.conf import settings
from geo.utils import social_query
from misc.basic_auth_decorator import logged_in_or_basicauth


from django.views.decorators.cache import cache_page


import logging

try:
    from notification import models as notification
except ImportError:
    notification = None



@login_required
def remove_storyline_attachment(request, id):
    storyline_attachment = StoryLineItemMedia.objects.get(pk=id)
    if storyline_attachment.storylineitem.creator == request.user:
        storyline_attachment.delete()
        return HTTPResponse(status=200, content="Removed")
    return HTTPResponse(status=400, content="Not Allowed")


@logged_in_or_basicauth()
def mobile_post(request):
    logging.debug("Uploading Experience")
    story_form = StoryForm(request.user, request.POST, request.FILES)
    if story_form.is_valid():
        story = story_form.save(request.user)
        return render_to_response("story/story-post-reply.html", {
            "story":story,
        }, context_instance=RequestContext(request))
    else:
        return HTTPResponse(status=400, content="Error")

@logged_in_or_basicauth()
def mobile_add_track(request, id):
    story = get_object_or_404(Story, pk=id)
    if request.POST:
        mobileForm = MobileClientGPSForm(request.POST)
        if mobileForm.is_valid():
            track = mobileForm.save(request.user, story)
            return render_to_response("story/story-post-reply.html", {
                "story":story,
                "track":track,
            }, context_instance=RequestContext(request))
        else:
            return HttpResponse(status=400, content="form not valid")
    else:
        return HttpResponse(status=400, content="only post allowed")

@logged_in_or_basicauth()
def mobile_add_post_to_story(request, id, template_name="story/story-post-reply.html"):
    logging.debug("Adding Post to Experience")
    story = get_object_or_404(Story, pk=id)
    if request.POST:
        form = MobileStoryLineItemForm(request.POST, request.FILES)
        if form.is_valid():
            storylineitem = form.save(request.user, story)
            storylineitem.story.save() #init bounding box calculation
            logging.debug("Finished Post")
            return render_to_response(template_name, {
                "story": story,
            }, context_instance=RequestContext(request))
        else:
            logging.debug("Form not valid")
            return HttpResponse(status=400, content="form not valid")
    else:
        return HttpResponse(status=400, content="only post allowed")
     
    
@login_required
def upload_gpx(request, id, template_name="story/gpx_upload.html"):
    story = get_object_or_404(Story, pk=id)
    if story.creator == request.user:
        form = GPXUploadForm(request.user)
        if request.method == "POST":
            try:
                form = GPXUploadForm(request.user, request.POST, request.FILES)
                if form.is_valid():
                    track = form.save()
                    track.set_story_reference(story)
                    return HttpResponse(status=200, content=track.get_geojson(), mimetype='text/html')
            except Exception, e:
                logging.warn(e)
                return HttpResponse(status=400, content="Could not parse GPX")

        return render_to_response(template_name, {
            "form": form,
        }, context_instance=RequestContext(request))
    else:
        return render_to_response("error.html", {
            "title": "error",
            "message": "not allowed",
        }, context_instance=RequestContext(request))


@login_required
def add_post_to_story(request, id, template_name="story/add_post_reply.html"):
    story = get_object_or_404(Story, pk=id)
    if request.POST:
        form = StoryLineItemForm(request.POST)
        if form.is_valid():
            storylineitem = form.save(request.user, story)
            storylineitem.story.save() #init bounding box calculation
            return render_to_response(template_name, {
                "story": story,
            }, context_instance=RequestContext(request))
        else:
            return HttpResponse(status=400, content="form not valid")
    else:
        return HttpResponse(status=400, content="only post allowed")
    
    
@login_required
def add_video_to_story(request, id):
    story = get_object_or_404(Story, pk=id)
    if story.creator == request.user:
        video = StoryVideoForm(request.POST)
        video = video.save(request.user)
        content_type = content_type = ContentType.objects.get_for_model(video)
        storylineitem = StoryLineItem.objects.get_or_create(story=story,
                                                            content_type=content_type,
                                                            object_id=video.id)
        return HttpResponse(status=200, content="Added")
    return HttpResponse(status=400, content="Could not parse GPX")


@login_required
def add_path_to_story(request, id):
    story = get_object_or_404(Story, pk=id)
    if story.creator == request.user:
        pathid = request.POST.get("pathid", None)
        if pathid:
            path = MGPXTrack.objects.get(pk=pathid)
            if path:
                story.tracks.add(path)
                story.save()
                return HttpResponse(status=200, content=path.get_geojson(), mimetype='text/html')
    return HttpResponse(status=400, content="something went wrong", mimetype='text/html')


@login_required
def remove_path_from_story(request, id):
    story = get_object_or_404(Story, pk=id)
    if story.creator == request.user:
        pathid = request.POST.get("pathid", None)
        content_type = request.POST.get("content_type", None)
        content_type_split = content_type.split(".")
        name = content_type_split[1].replace("_", " ")
        
        content_type = get_object_or_404(ContentType,
                                     app_label=content_type_split[0],
                                     name=name)

        if pathid:
            path = content_type.model_class().objects.get(pk=pathid)
            if path:
                path.content_type = None
                path.object_id = None
                path.save()
                return HttpResponse(status=200, content="Ok", mimetype='text/html')
    return HttpResponse(status=400, content="something went wrong", mimetype='text/html')


@login_required
def edit_story_title(request, id):
    story = get_object_or_404(Story, pk=id)
    story.title = request.POST.get("title")
    story.save()
    return HttpResponse(status=200, content="%s <a href='#'>(edit)</a>"%story.title, mimetype='text/html')
    
    
@login_required
def create(request, form_class=StoryForm, template_name="story/edit.html"):
    if request.method == "POST":
        story_form = form_class(request.user, request.POST, request.FILES)
        if story_form.is_valid():
            story = story_form.save(request.user)
            return HttpResponseRedirect(reverse("story_edit", args=(story.id,)))
        else:
            return HttpResponse(status=400, content="Title has to be specified")
    elif request.method == "GET":
        story = Story(creator=request.user)
        story.save()
        return HttpResponseRedirect(reverse("story_edit", args=(story.id,)))
        
    return HttpResponse(status=400, content="Only Post allowed")

@login_required
def delete(request, id, template_name=""):
    story = get_object_or_404(Story, pk=id)
    if story.creator == request.user:
        story.delete()

    success_url = request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(success_url)
    
    
@login_required
def your_stories(request, template_name="story/your_stories.html"):
    unpublished_stories = request.user.stories.filter(status=Story.STATUS_DRAFT)\
                                .order_by("-creation_date").all()
    published_stories = request.user.stories.filter(status=Story.STATUS_PUBLIC)\
                                .order_by("-creation_date").all()
    return render_to_response(template_name, {
        "published_stories": published_stories,
        "unpublished_stories": unpublished_stories,
        "viewed_user": request.user,
    }, context_instance=RequestContext(request))

def user_stories(request, username, template_name="story/user_stories.html"):
    user = get_object_or_404(User, username=username)
    stories = user.stories.all().order_by("-creation_date")
    return render_to_response(template_name, {
        "stories": stories,
        "viewed_user": user,
    }, context_instance=RequestContext(request))

@login_required
def edit(request, id, template_name="story/edit.html"):
    story = get_object_or_404(Story, pk=id)
    
    if story.creator == request.user:
        if request.POST:
            create_activity_item("edited_story", request.user, story)
            # save
            form = StoryEditForm(request.POST, instance=story)

            if form.is_valid():
                form.save(request.user)
                return HttpResponse(status=200, content="<div class='ajax-message'>Successfully stored Changes</div>")
            else:
                return HttpResponse(status=400, content="Error")
        else:
            return render_to_response(template_name, {
                "story": story,
                "post_form": StoryPostForm(),
                "video_form": StoryVideoForm(),
                "gpx_upload_form": GPXUploadForm(request.user),
                "story_edit_form": StoryEditForm(instance=story),
            }, context_instance=RequestContext(request))
    else:
        return render_to_response("error.html", {
            "title": _("You are not authorized"),
            "text": _("Only the creator of the Story can edit it")
        }, context_instance=RequestContext(request))


@login_required
def preview(request, id, template_name="story/preview.html"):
    story = get_object_or_404(Story, pk=id)
    if story.creator == request.user:
        return render_to_response(template_name, {
            "story": story,
            "post_form": StoryPostForm(),
            "video_form": StoryVideoForm(),
            "gpx_upload_form": GPXUploadForm(request.user),
            "story_edit_form": StoryEditForm(instance=story),
        }, context_instance=RequestContext(request))
    else:
        return render_to_response("error.html", {
            "title": _("You are not authorized"),
            "text": _("Only the creator of the Story can edit it")
        }, context_instance=RequestContext(request))


@login_required
def publish(request, id, template_name="story/publish.html"):
    story = get_object_or_404(Story, id=id)
    if story.creator == request.user:
        form = StoryEditForm(request.POST, instance=story)
        if form.is_valid():
            story = form.save(request.user)
            story.status = story.STATUS_PUBLIC
            story.save()
            
            return render_to_response(template_name, {
                "story": story,
                "post_form": StoryPostForm(),
                "video_form": StoryVideoForm(),
                "gpx_upload_form": GPXUploadForm(request.user),
                "story_edit_form": StoryEditForm(instance=story),
            }, context_instance=RequestContext(request))
        else:
            return render_to_response(template_name, {
                "story": story,
            }, context_instance=RequestContext(request))
    else:
        return render_to_response("error.html", {
            "title": _("You are not authorized"),
            "text": _("Only the creator of the Story can edit it")
        }, context_instance=RequestContext(request))


def storyline(request, id, template_name="story/storyline.html"):
    story = get_object_or_404(Story, pk=id)
    return render_to_response(template_name, {
        "story": story,
    }, context_instance=RequestContext(request))


@login_required
def reorder_storyline(request, id, template_name="story/reorder_success.html"):
    story = get_object_or_404(Story, pk=id)

    if story.creator == request.user:
        # get the list of position changes
        try:
            newPosition = request.POST.get("newPosition", False)
            oldPosition = request.POST.get("oldPosition", False)
            if newPosition is not False and oldPosition is not False:
                newPosition = int(newPosition)
                oldPosition = int(oldPosition)
            else:
                return HttpResponse(status=400, content="newPosition and oldPosition are required")
        except:
            return HttpResponse(status=400, content="newPosition and oldPosition have to be of type interger")

        storyline = story.storyline.order_by('position')

        if newPosition >= 0 and newPosition < len(storyline) and oldPosition >= 0 and oldPosition < len(storyline):
            item = storyline[int(oldPosition)]
            item.position = int(newPosition)
            item.save()
        else:
            return HttpResponse(status=400, content="Index out of range")

        return HttpResponse(status=200, content="Ok")
    else:
        return HttpResponse(status=400, content="Not Allowed") 

#@cache_page(60 * 15)
def view(request, slug=None, template_name="story/view.html"):
    story = get_object_or_404(Story, slug=slug)
    position_lat = request.GET.get("lat", None)
    position_lng = request.GET.get("lng", None)
    zoom = request.GET.get("zoom", None)
    storyline_index = request.GET.get("storyline-index", 0)
    custom_css = request.GET.get("custom-css", None)
    
    return render_to_response(template_name, {
        "story": story,
        "position_lat": position_lat,
        "position_lng": position_lng,
        "zoom": zoom,
        "storyline_index": storyline_index,
        "custom_css": custom_css,
    }, context_instance=RequestContext(request))

#@cache_page(60 * 15)
def view_id(request, id, template_name="story/view.html"):
    story = get_object_or_404(Story, pk=id)
    position_lat = request.GET.get("lat", None)
    position_lng = request.GET.get("lng", None)
    zoom = request.GET.get("zoom", None)
    storyline_index = request.GET.get("storyline-index", 0)
    custom_css = request.GET.get("custom-css", None)
    
    return render_to_response(template_name, {
        "story": story,
        "position_lat": position_lat,
        "position_lng": position_lng,
        "zoom": zoom,
        "storyline_index": storyline_index,
        "custom_css": custom_css,
    }, context_instance=RequestContext(request))
    
    
@login_required
def select_main_image(request, id=None, template_name="story/select_main_image.html"):
    story = get_object_or_404(Story, pk=id)
    return render_to_response(template_name, {
        "story": story,
    }, context_instance=RequestContext(request))


@login_required
def set_main_image(request, id=None, photo_id=None):
    story = get_object_or_404(Story, pk=id)
    if story.creator == request.user:
        photo = Image.objects.get(pk=photo_id)
        storyimages = StoryImage.objects.filter(story=story).all()
        if storyimages:
            for image in storyimages:
                image.delete()
        
        story_image.save()

        create_activity_item("edited_story", request.user, story)
        
        return HttpResponseRedirect(reverse("story_edit", args=(story.slug,)))
    else:
        return HttpResponse(status=400, content="Error")


def story_line_item(request, id=None, template_name="story/storylineitem.html"):
    story = get_object_or_404(Story, pk=id)
    index = request.GET.get("index", False)
    
    error_text = "index is required"
    if not index == False:
        index = int(index)
        if index >= 0 and index < story.storyline.count():
            return render_to_response(template_name, {
                "item": story.storyline.all()[index],
            }, context_instance=RequestContext(request))

    return HttpResponse(status=200, content="Does not exist")


def stories_in_area(request, template_name="story/story_list.html"):
    x1 = request.POST.get("x1", False)
    x2 = request.POST.get("x2", False)
    y1 = request.POST.get("y1", False)
    y2 = request.POST.get("y2", False)
    offset = int(request.POST.get("offset", 0))
    count = int(request.POST.get("count", 4))
    user_id = request.POST.get("user_id", False)
    network = request.POST.get("network", False)
    
    finalcount = offset+count
    stories = Story.objects.search_in_area(x1, y1, x2, y2)
    
    if user_id:
        stories = social_query(get_object_or_404(User, pk=user_id), network, stories)
    
    return render_to_response(template_name, {
        "stories": stories[offset:finalcount],
    }, context_instance=RequestContext(request))
    
    
def add_to_storyline(request, id, template_name="story/add_to_storyline.html"):
    story = get_object_or_404(Story, pk=id)
    if request.user == story.creator:
        #array of contenttype and ids
        objects = request.POST.getlist("added_objects")
        for object in objects:
            identifier = object.split(".")
            object_class = models.get_model(identifier[0], identifier[1])
            object = object_class.objects.get(pk=identifier[2])
            content_type = ContentType.objects.get_for_model(object)
            StoryLineItem.objects.get_or_create(story=story,
                                                  content_type=content_type,
                                                  object_id=object.id)
        return render_to_response(template_name, {
        }, context_instance=RequestContext(request))
    else:
        return  render_to_response(template_name, {
            "title": "Error",
            "message": "Not Allowed",
        }, context_instance=RequestContext(request))
    

def remove_from_storyline(request, story_id, id, template_name=""):
    story = get_object_or_404(Story, pk=story_id)
    if request.user == story.creator:
        storyline_item = get_object_or_404(StoryLineItem, pk=id)
        if storyline_item.story == story:
            storyline_item.delete()
            return HttpResponse(status=200, content="ok")
    return HttpResponse(status=400, content="error")


def add_post_to_story_screen(request, id, template_name="story/add_post.html"):
    story = get_object_or_404(Story, pk=id)
    return render_to_response(template_name, {"post_form":StoryPostForm(),
                                              "story": story},
                              context_instance=RequestContext(request))
    
    
def add_video_to_story_screen(request, id, template_name="story/add_video.html"):
    story = get_object_or_404(Story, pk=id)
    return render_to_response(template_name, {"video_form":StoryVideoForm(),
                                              "story": story},
                              context_instance=RequestContext(request))
    

def storylineitem_attachments(request, template_name="story/attachment_list.html"):
    itemsUIDs = request.GET.get("items")
    itemsUIDs = itemsUIDs.split(",")
    items = []
    from misc.utils import get_target_object
    for uuid in itemsUIDs:
        items.append(get_target_object(uuid))
    return render_to_response(template_name, {"items_list":items},
                                context_instance=RequestContext(request))
    
def edit_storylineitem(request, template_name="story/edit_storylineitem.html"):
    if request.POST:
        submitted = request.POST.get("action", False)
        storylineitem = get_object_or_404(StoryLineItem, pk=request.POST.get("storylineitemid"))
        if submitted:
            return render_to_response(template_name, {"storylineitem":storylineitem,
                                                      'submitted':True},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response(template_name, {"storylineitem":storylineitem},
                                      context_instance=RequestContext(request))
    else:
        storylineitem = get_object_or_404(StoryLineItem, pk=request.GET.get("storylineitemid"))
        return render_to_response(template_name, {"storylineitem":storylineitem},
                                  context_instance=RequestContext(request))