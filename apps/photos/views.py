from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, get_host, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from activity_stream.models import create_activity_item

from photologue.models import *
from photos.models import Image
from photos.forms import PhotoUploadForm, PhotoEditForm, PhotoFlashUploadForm
from projects.models import Project

from story.models import Story, StoryLineItem
from django.contrib.contenttypes.models import ContentType

def upload(request, form_class=PhotoUploadForm,
        template_name="photos/upload.html"):
    """
    upload form for photos
    """
    photo_form = form_class()
    if request.method == 'POST':
        if request.POST["action"] == "upload":
            photo_form = form_class(request.user, request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.member = request.user
                photo.save()
                photo.rotate_to_exif()
                request.user.message_set.create(message=_("Successfully uploaded photo '%s'") % photo.title)

                #create_activity_item("uploaded_pictures", request.user, photo)

                return HttpResponseRedirect(reverse('photo_details', args=(photo.id,)))

    return render_to_response(template_name, {
        "photo_form": photo_form,
    }, context_instance=RequestContext(request))
upload = login_required(upload)


def flash_upload(request, form_class=PhotoFlashUploadForm, template_name="photos/flash_success.html"):
    # reestablish session
    #import pdb; pdb.set_trace()
    session = get_object_or_404(Session, session_key=request.POST.get('sessionid'))
    session_data = session.get_decoded()
    user_id = session_data['_auth_user_id']
    request.user = get_object_or_404(User, pk = user_id)
    request.FILES['image'] = request.FILES['Filedata']
    
    if request.method == 'POST':
        
        photo_form = form_class(request.user, request.POST, request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.title = request.FILES['image'].name
            photo.member = request.user
            photo.save()
            photo.rotate_to_exif()
            #request.user.message_set.create(message=_("Successfully uploaded photo '%s'") % photo.title)

            #create_activity_item("uploaded_pictures", request.user, photo)

            if request.POST.get("story_id", False):
                story = Story.objects.filter(id=request.POST.get("story_id"))
                if story:
                    story = story[0]
                    content_type = ContentType.objects.get_for_model(story)
                    story.storyline.create(content_type=content_type, object_id=photo.id, content_object=photo)
    
    return render_to_response(template_name, {
        "photo": photo,
    }, context_instance=RequestContext(request))


def yourphotos(request, template_name="photos/yourphotos.html"):
    """
    photos for the currently authenticated user
    """
    photos = Image.objects.filter(member=request.user).order_by("-date_added")
    return render_to_response(template_name, {
        "photos": photos,
    }, context_instance=RequestContext(request))
yourphotos = login_required(yourphotos)

def photos(request, template_name="photos/latest.html"):
    """
    latest photos
    """
    photos = Image.objects.filter(is_public=True).order_by("-date_added")
    return render_to_response(template_name, {
        "photos": photos,
    }, context_instance=RequestContext(request))

def details(request, id, template_name="photos/details.html"):
    """
    show the photo details
    """
    other_user = request.user

    photo = get_object_or_404(Image, id=id)
    
    title = photo.title
    host = "http://%s" % get_host(request)
    if photo.member == request.user:
        is_me = True
    else:
        is_me = False

    return render_to_response(template_name, {
        "host": host, 
        "photo": photo,
        "is_me": is_me, 
        "other_user": other_user,
    }, context_instance=RequestContext(request))

def memberphotos(request, username, template_name="photos/memberphotos.html"):
    """
    Get the members photos and display them
    """
    user = get_object_or_404(User, username=username)
    photos = Image.objects.filter(member__username=username, is_public=True).order_by("-date_added")
    return render_to_response(template_name, {
        "photos": photos,
        "viewed_user": user,
    }, context_instance=RequestContext(request))
memberphotos = login_required(memberphotos)

def edit(request, id, form_class=PhotoEditForm,
        template_name="photos/edit.html"):
    photo = get_object_or_404(Image, id=id)
    

    if request.method == "POST":
        if photo.member != request.user:
            request.user.message_set.create(message="You can't edit photos that aren't yours")
            return HttpResponseRedirect(reverse('photo_details', args=(photo.id,)))
        if request.POST["action"] == "update":
            photo_form = form_class(request.user, request.POST, instance=photo)
            if photo_form.is_valid():
                photoobj = photo_form.save(commit=False)
                photoobj.save()
                request.user.message_set.create(message=_("Successfully updated photo '%s'") % photo.title)
                return HttpResponseRedirect(reverse('photo_details', args=(photo.id,)))
        else:
            photo_form = form_class(instance=photo)

    else:
        photo_form = form_class(instance=photo)

    return render_to_response(template_name, {
        "photo_form": photo_form,
        "photo": photo
    }, context_instance=RequestContext(request))
edit = login_required(edit)

def destroy(request, id):
    photo = Image.objects.get(pk=id)
    title = photo.title
    if photo.member != request.user:
        request.user.message_set.create(message="You can't delete photos that aren't yours")
        return HttpResponseRedirect(reverse("photos_yours"))

    if request.method == "POST" and request.POST["action"] == "delete":
        photo.delete()
        request.user.message_set.create(message=_("Successfully deleted photo '%s'") % title)
    return HttpResponseRedirect(reverse("photos_yours"))
destroy = login_required(destroy)

def rotate(request, id, redirect=True):
    photo = Image.objects.get(pk=id)
    photo.clear_cache()
    if photo.member == request.user:
        rotation = request.GET.get("rotation", False)
        if rotation:
            photo.rotate(float(rotation))
    
    if redirect:
        return HttpResponseRedirect(reverse("photo_details", args=(photo.id,)))
    else:
        return HttpResponse(status=200, content="ok")

def photo_selector(request, username, template_name="photos/photo_selector.html"):
    user = get_object_or_404(User, username=username)
    return render_to_response(template_name, {
        "viewed_user": user,
        "post_url": request.GET.get("post_url"),
        "callback": request.GET.get("callback"),
    }, context_instance=RequestContext(request))


def photo_selector_list(request, username, template_name="photos/photo_selector_list.html"):
    user = get_object_or_404(User, username=username)
    photos = Image.objects.filter(member__username=username).order_by("-date_added")
    dynamic_div = 'dynamic_list_div'
    ref_url = reverse('photo_selector_list',args=(username,))
    return render_to_response(template_name, {
        "viewed_user": user,
        "photos": photos,
        "ref_url": ref_url,
        "dynamic_div": dynamic_div,
    }, context_instance=RequestContext(request))
    
    
    