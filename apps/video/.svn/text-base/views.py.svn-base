from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from blog.models import Post;
from django.contrib.auth.models import User
from oembed.core import fetch
from oembed.core import re_parts
from video.forms import VideoImportForm, VideoForm, VideoUploadForm, VideoEditForm
from video.models import Video
from oembed.models import ProviderRule
import re
from django.conf import settings
from django.template.loader import render_to_string
from video.rest.restful_lib import Connection
import md5
from xml.dom.minidom import parseString
from video.rest.vimeoPy import VimeoClient
from video.models import VimeoToken
import tempfile
from tagging.utils import parse_tag_input
from mailer import send_mail, mail_admins
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

try:
    import simplejson
except ImportError:
    from django.utils import simplejson

def index(request):
    # get featured videos
    # last ten videos
    videos = Video.objects.all();
    return render_to_response('video/index.html', {
        'videos': videos
    }, context_instance=RequestContext(request))

def your_videos(request):
    videos = Video.objects.filter(creator=request.user);
    return render_to_response('video/index.html', {
        'videos': videos
    }, context_instance=RequestContext(request))
    
def show(request, id):
    video = Video.objects.get(pk=id)
    return render_to_response('video/show.html', {
        'is_me': video.creator.id==request.user.id,
        'video': video,
        #'projects': p,
    }, context_instance=RequestContext(request))

@login_required
def create(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            return render_to_response('video/successful_import.html', {},
                                      context_instance=RequestContext(request))
    else:
        form = VideoForm()
        importForm = VideoImportForm()

        return render_to_response('video/create.html', {
            'form': form,
            'importForm': importForm,
            }, context_instance=RequestContext(request))

        
def vimeo_callback(request, template_name='video/vimeo_auth_callback.html'):
    if(request.GET['frob']):
        vimeoClient = VimeoClient(settings.VIMEO_API_KEY,
                                  settings.VIMEO_API_SECRET)
        rsp = vimeoClient.call('vimeo.auth.getToken',
                               {'frob': request.GET['frob']})
        if(rsp.attributes['stat'].value == 'ok'):
            token = rsp.getElementsByTagName("token")[0].childNodes[0].nodeValue
            VimeoToken.objects.all().delete();
            vimeoToken = VimeoToken(name="mainAccount", token=token)
            vimeoToken.save()
            return render_to_response(template_name, {
                "success":True
            }, context_instance=RequestContext(request))
        else:
            return render_to_response(template_name, {
                "success":False
            }, context_instance=RequestContext(request))

@login_required
def upload_video(request, template_name='video/upload.html'):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)

        if form.is_valid():
            vimeoClient = VimeoClient(settings.VIMEO_API_KEY,
                                      settings.VIMEO_API_SECRET)
            tempVideo = open(tempfile.mktemp(".AVI"), 'wb+')
            for chunk in form.files['video'].chunks():
                tempVideo.write(chunk)
            try:
                ticked_id = vimeoClient.upload(tempVideo.name)
            except Exception, inst:
                mail_admins("Error Uploading Video",
                            "Vimeo Video konnte nicht hochgeladen werden: "\
                            +str(inst.args))
                return render_to_response("video/upload_error.html", {
                }, context_instance=RequestContext(request))

            tempVideo.close()
            if ticked_id:
                video_id = vimeoClient.check_upload_status(ticked_id)
                if video_id:
                    #get thumbnail url
                    rsp = vimeoClient.call("vimeo.videos.getThumbnailUrl",
                                           {"video_id": video_id,
                                            "size":"160x120"} )
                    thumbnail_url = rsp.getElementsByTagName("thumbnail")[0]\
                                                        .childNodes[0].nodeValue
                    #set the values
                    video = Video(creator=request.user,
                      import_url="http://vimeo.com/"+video_id,
                      was_uploaded=True,
                      is_viewable=False,
                      external_id=video_id,
                      ticket_id=ticked_id,
                      comment=form.cleaned_data['comment'],
                      title=form.cleaned_data['title'],
                      tags=form.cleaned_data['tags'],
                      thumbnail_url=thumbnail_url
                    )
                    video.save();
                    
                    rsp = vimeoClient.call("vimeo.videos.setTitle", {
                                            "title": form.cleaned_data['title'],
                                            "video_id": video_id
                                            } )
                    if(rsp.attributes['stat'].value!="ok"):
                        mail_admins("Error",
                                    "Vimeo Titel konnte nicht gesetzt werden:\
                                     Video_id: "+str(video.pk))

                    rsp = vimeoClient.call("vimeo.videos.setCaption", {
                                    "caption": form.cleaned_data['comment'],
                                    "video_id": video_id
                                } )
                    if(rsp.attributes['stat'].value!="ok"):
                        mail_admins("Error",
                                    "Vimeo Caption konnte nicht gesetzt werden:\
                                    Video_id: "+str(video.pk))

                    rsp = vimeoClient.call("vimeo.videos.setPrivacy",
                                           {"privacy": "anybody",
                                            "video_id": video_id} )
                    if(rsp.attributes['stat'].value!="ok"):
                        mail_admins("Error",
                                    "Vimeo Privacy konnte nicht gesetzt werden:\
                                    Video_id: "+str(video.id))

                    if form.cleaned_data['tags']:
                        tags = parse_tag_input(video.tags)
                        tags = ",".join(tags)
                        rsp = vimeoClient.call("vimeo.videos.addTags",
                                               {"tags": tags,
                                                "video_id": video_id} )
                        if(rsp.attributes['stat'].value!="ok"):
                            mail_admins("Error",
                                        "Vimeo Tags konnten nicht gesetzt \
                                        werden: Video_id: "+str(video.id))
                            
                    return render_to_response("video/upload_success.html", {
                       "video": video,
                    }, context_instance=RequestContext(request))

            # an error has occurred
            return render_to_response("video/upload_error.html", {
            }, context_instance=RequestContext(request))
        else:
            request.user.message_set.create(message=_("Video '%s' was \
                                         successfully uploaded!") % video.title)
            return HttpResponseRedirect(reverse('show_video', args=(video.id,)))

@login_required
def vimeo_save_video(request, ticketId):
    vimeoClient = VimeoClient(settings.VIMEO_API_KEY, settings.VIMEO_API_SECRET)
    rsp = vimeoClient.call('vimeo.videos.checkUploadStatus',
                           {'ticket_id': ticketId})

    if(rsp.attributes['stat'].value=="ok"):
        id = rsp.getElementsByTagName("ticket")[0].attributes["video_id"].value
        video = Video(creator= request.user,
                      import_url="http://vimeo.com/"+id,
                      imported=False,
                      thumbnail_url="",
                      title="",
                      )
        return render_to_response("video/failed_ticket.html", {
        }, context_instance=RequestContext(request))
    else:
        return render_to_response("video/failed_ticket.html", {
        }, context_instance=RequestContext(request))

@login_required
def import_video(request):
    if request.method == 'POST':
        form = VideoImportForm(request.POST)
        if form.is_valid():
            rules = list(ProviderRule.objects.all())
            patterns = [re.compile(r.regex) for r in rules]
            for i, part in re_parts(patterns, form.cleaned_data['url']):
                rule = rules[i]
                FORMAT = getattr(settings, "OEMBED_FORMAT", "json")
                url = u"%s?url=%s&maxwidth=%s&maxheight=%s&format=%s" % (
                    rule.endpoint, part, 600, 400, FORMAT
                )

                resp = simplejson.loads(fetch(url))
                replacement = render_to_string('oembed/%s.html' % resp['type'],
                                               {'response': resp})

            # TODO: this should be in oembed, bit dont want to modify it now
            if(resp):
                if(resp.has_key('thumbnail_url')):
                   thumbnail_url = resp['thumbnail_url']
                else:
                   p = re.compile('v=([^&]+)')
                   m = p.search(form.cleaned_data['url'])
                   id = m.group()
                   id = id.replace("v=","")
                   thumbnail_url = "http://img.youtube.com/vi/"+id+"/1.jpg"
                   #import pdb; pdb.set_trace()

                    
                video = Video(creator= request.user,
                              import_url=form.cleaned_data['url'],
                              was_uploaded=False,
                              thumbnail_url=thumbnail_url,
                              title=form.cleaned_data['title'],
                              )
                video.save()
                request.user.message_set.create(message=_("Video '%s' was \
                                         successfully imported!") % video.title)
                return HttpResponseRedirect(reverse('show_video',
                                                    args=(video.id,)))
            else:
                return render_to_response('video/unsuccessful_import.html', {
                                'url': form.cleaned_data['url']
                                }, context_instance=RequestContext(request));
    else:
        form = VideoImportForm(request.POST)
        return render_to_response("", {'form': form},
                                  context_instance=RequestContext(request))


@login_required
def preview_import(request):
     if request.method == 'POST':
        form = VideoImportForm(request.POST)
        if form.is_valid():
            return render_to_response("video/preview.html",
                                      {'url': form.cleaned_data['url']},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response("video/preview-error.html",
                                      {'form': form},
                                      context_instance=RequestContext(request))

def search(request, template_name='video/search.html'):
    return render_to_response(template_name, {
    }, context_instance=RequestContext(request))

@login_required   
def edit(request, id, template_name='video/edit.html'):
    video = get_object_or_404(Video, id=id)
    if request.method == 'POST':
        video_form = VideoEditForm(request.user, request.POST, instance=video)
        if video_form.is_valid():
            video_form.save()
            return HttpResponseRedirect(reverse('show_video', args=(id,)))
        else:
             return render_to_response(template_name, {
                "form": video_form,
                "video": video,
            }, context_instance=RequestContext(request))
    else:
        return render_to_response(template_name, {
            "form": VideoEditForm(instance=video),
            "video": video,
        }, context_instance=RequestContext(request))
    
@login_required
def destroy(request, id, template_name='video/delete.html'):
    video = Video.objects.get(pk=id)
    if video.creator.id == request.user.id:
        video.delete()
        return render_to_response(template_name, {
        }, context_instance=RequestContext(request))
    else:
       return show(request, video.id) 

def oembed_video_url(request, id, template_name='video/profile_video.html'):
    video = get_object_or_404(Video, id=id)
    return render_to_response(template_name, {
        "import_url": video.import_url,
    }, context_instance=RequestContext(request))
    

def video_selector_list(request, username,
                        template_name="video/video_selector_list.html"):
    user = get_object_or_404(User, username=username)
    videos = Video.objects.filter(creator__username=username)\
                                                        .order_by("-date_added")
    dynamic_div = 'dynamic_video_list_div'
    ref_url = reverse('video_selector_list',args=(username,))
    return render_to_response(template_name, {
        "viewed_user": user,
        "videos": videos,
        "ref_url": ref_url,
        "callback_function": request.GET.get("callback"),
    }, context_instance=RequestContext(request))