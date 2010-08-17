from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count, Q
from maptales_app.models import PrivateBetaEmail
from mailer import send_mail, mail_admins

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from django.views.decorators.cache import cache_page
from account.forms import LoginForm, SignupForm
from django.contrib import auth

try:
    import simplejson
except ImportError:
    from django.utils import simplejson

def mobile_login(request, form_class=LoginForm, template_name="account/login.html"):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.login(request):
            return HttpResponse(status=200, content="Ok")
    return HttpResponse(status=400, content="Only post allowed")


def mobile_signup(request, form_class=SignupForm, success_url=None):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)    
            return HttpResponse(status=200, content="Ok")
        else:
            returnText = ""
            for error in form.errors:
                text = "Error: %s"%(form.errors[error].as_text(),)
            return HttpResponse(status=400, content=text)
    else:
        return HttpResponse(status=400, content="Only post allowed")


#@cache_page(60 * 15)
def index(request):
    #if request.user.is_authenticated():
    #    return HttpResponseRedirect(reverse("activity_stream", args=(request.user.username,)))

    return render_to_response('maptales_app/index.html', {
    }, context_instance=RequestContext(request))


def private_beta_email(request):
    email = request.POST.get("email")
    PrivateBetaEmail.objects.create(email=email)
    mail_admins("new private beta request", "%s total: %s"%(email, PrivateBetaEmail.objects.count()), fail_silently=False)
    return render_to_response('maptales_app/private_beta_thanks.html', {
    }, context_instance=RequestContext(request))

def passphrase_check(request):
    if request.POST.get("passphrase") == "geek154":
        from account.views import signup
        return signup(request)
    else:
        return render_to_response('maptales_app/passphrase_check_invalid.html', {
        }, context_instance=RequestContext(request))
    
def search(request):
    return render_to_response('maptales_app/search.html', {
    }, context_instance=RequestContext(request))


def handler500(request):
    return render_to_response('500.html', {
    }, context_instance=RequestContext(request))

#@cache_page(60 * 15)
def iphone(request):
    return render_to_response('iphone.html', {
    }, context_instance=RequestContext(request))

def global_activity(request):
    return render_to_response('maptales_app/global_activity.html', {}, context_instance=RequestContext(request))

def user_list(request, queryset=User.objects.all(),
              template_name="maptales_app/user_list.html"):
    filter_string = request.GET.get('filter')
    startswith_string = request.GET.get('startswith')
    
    users = queryset
    if filter_string and users:
        users = queryset.filter(Q(username__icontains=filter_string) 
                                    | Q(profile__first_name__icontains=filter_string)
                                    | Q(profile__last_name__icontains=filter_string))
    if startswith_string and users:
        users = queryset.filter(Q(username__istartswith=startswith_string) 
                                    | Q(profile__last_name__istartswith=startswith_string)
                                    | Q(profile__first_name__istartswith=filter_string))
    if users:
        users = users.annotate(storycount=Count('stories')).order_by("-storycount") #.order_by("username").order_by("profile__last_name")
        
    context = {
                "users": users,
                "filter": filter_string,
                "startswith": startswith_string,
            }
    return render_to_response(template_name, context, context_instance=RequestContext(request))

def switch_user(request, template_name="maptales_app/switch_user.html"):
    from django.contrib.auth import load_backend, login, BACKEND_SESSION_KEY
    if request.user.is_superuser or request.session["is_switched_admin"]:
        if request.GET.get("user_id", False):
            backend_path = request.session[BACKEND_SESSION_KEY]
            backend = load_backend(backend_path)
            user = backend.get_user(request.GET.get("user_id"))
            user.backend = backend
            login(request, user)
            request.session[BACKEND_SESSION_KEY] = backend_path
            request.session["is_switched_admin"] = True
            return HttpResponseRedirect(reverse("home"))
        else:
            return user_list(request, template_name=template_name)
    else:
        return render_to_response("error.html", {
            "title": "Security Error",
            "text": "Only admins can do this",
        }, context_instance=RequestContext(request))

