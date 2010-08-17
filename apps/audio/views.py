from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, get_host
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from audio.forms import AudioUploadForm, AudioFlashUploadForm, AudioEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from audio.models import Audio


def index(request, template_name="audio/index.html"):
    audios = Audio.objects.all();
    return render_to_response(template_name, {
        "audios":audios,
    }, context_instance=RequestContext(request))


def upload(request, form_class=AudioUploadForm,
        template_name="audio/upload.html"):
    """
    upload form for audios
    """
    audio_form = form_class()
    if request.method == 'POST':
        if request.POST["action"] == "upload":
            audio_form = form_class(request.user, request.POST, request.FILES)
            if audio_form.is_valid():
                audio = audio_form.save(commit=False)
                audio.creator = request.user
                if not audio.title:
                    audio.title = request.FILES['audio_file'].name
                audio.save()
                #request.user.message_set.create(message=_("Successfully uploaded audio '%s'") % audio.title)
                return render_to_response("audio/upload_success.html", {
                    "audio": audio,
                }, context_instance=RequestContext(request))

    return render_to_response(template_name, {
        "audio_form": audio_form,
    }, context_instance=RequestContext(request))
upload = login_required(upload)


def flash_upload(request, form_class=AudioFlashUploadForm, template_name="audio/upload.html"):

    # reestablish session
    session = get_object_or_404(Session, session_key=request.POST.get('sessionid'))
    session_data = session.get_decoded()
    user_id = session_data['_auth_user_id']
    request.user = get_object_or_404(User, pk = user_id)
    request.FILES['audio_file'] = request.FILES['Filedata']

    if request.method == 'POST':
        audio_form = form_class(request.user, request.POST, request.FILES)
        if audio_form.is_valid():
            audio = audio_form.save(commit=False)
            audio.member = request.user
            audio.save()
            request.user.message_set.create(message=_("Successfully uploaded audio '%s'") % audio.title)
            return HttpResponseRedirect(reverse('audio_details', args=(audio.id,)))


def details(request, id, template_name="audio/details.html"):
    audio = get_object_or_404(Audio, id=id)
    return render_to_response(template_name, {
        "audio": audio,
    }, context_instance=RequestContext(request))

def destroy(request, id, template_name="audio/destroy.html"):
    audio = get_object_or_404(Audio, id=id)
    if request.POST:
        audio.delete()
        return render_to_response("audio/destroyed.html", {
        }, context_instance=RequestContext(request))
    else:
        return render_to_response(template_name, {
            "audio": audio,
        }, context_instance=RequestContext(request))

def edit(request, id, form_class=AudioEditForm, template_name="audio/edit.html"):
    audio = get_object_or_404(Audio, id=id)
    if request.POST:
        form = form_class(request.user, request.POST, request.FILES)
        new_audio = form.save(commit=False)
        audio.title = new_audio.title
        audio.cover = new_audio.cover
        audio.save();
        return HttpResponseRedirect(reverse('audio_details', args=(id,)))
    else:
        form = form_class(request.user,instance=audio)
        return render_to_response(template_name, {
            "audio": audio,
            "form": form,
        }, context_instance=RequestContext(request))