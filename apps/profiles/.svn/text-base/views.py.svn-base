from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from friends.forms import InviteFriendForm
from friends.models import FriendshipInvitation, Friendship

from profiles.models import Profile
from profiles.forms import ProfileForm
from mailer import send_mail, mail_admins

from avatar.templatetags.avatar_tags import avatar
from django.forms.models import   ModelMultipleChoiceField
from django.contrib.auth.decorators import login_required

from profiles.forms import LocationUpdateForm

try:
    from notification import models as notification
except ImportError:
    notification = None

@login_required
def profile_privacy(request, template_name="profiles/privacy.html"):
    return render_to_response(template_name, {
    }, context_instance=RequestContext(request))
    
@login_required
def profile_notification(request, template_name="profiles/notifications.html"):
    return render_to_response(template_name, {
    }, context_instance=RequestContext(request))

    
@login_required
def update_location(request):
    if(request.POST):
        form = LocationUpdateForm(request.POST)
        if form.is_valid():
            form.save(request.user);
            return HttpResponse(status=200, content="set")
        else:
            return HttpResponse(status=400, content="error")

def profiles(request, template_name="profiles/profiles.html"):
    return render_to_response(template_name, {
        "users": User.objects.all().order_by("-date_joined"),
    }, context_instance=RequestContext(request))

def friends(request, username, template_name="profiles/friends.html"):
    other_user = get_object_or_404(User, username=username)
    if request.user.is_authenticated():
        is_friend = Friendship.objects.are_friends(request.user, other_user)
        other_friends = Friendship.objects.friends_for_user(other_user)
        if request.user == other_user:
            is_me = True
        else:
            is_me = False

    return render_to_response(template_name, {
        "is_me": is_me,
        "is_friend": is_friend,
        "other_friends": other_friends,
    }, context_instance=RequestContext(request))


def profile(request, username, template_name="profiles/profile.html"):
    other_user = get_object_or_404(User, username=username)
    if request.user.is_authenticated():
        is_friend = Friendship.objects.are_friends(request.user, other_user)
        other_friends = Friendship.objects.friends_for_user(other_user)
        if request.user == other_user:
            is_me = True
        else:
            is_me = False
    else:
        other_friends = []
        is_friend = False
        is_me = False
    
    if is_friend:
        invite_form = None
        previous_invitations_to = None
        previous_invitations_from = None
    else:
        if request.user.is_authenticated() and request.method == "POST":
            if request.POST["action"] == "invite":
                invite_form = InviteFriendForm(request.user, request.POST)
                if invite_form.is_valid():
                    invite_form.save()
            else:
                invite_form = InviteFriendForm(request.user, {
                    'to_user': username,
                    'message': ugettext("Let's be friends!"),
                })
                if request.POST["action"] == "accept": # @@@ perhaps the form should just post to friends and be redirected here
                    invitation_id = request.POST["invitation"]
                    try:
                        invitation = FriendshipInvitation.objects.get(id=invitation_id)
                        if invitation.to_user == request.user:
                            invitation.accept()
                            request.user.message_set.create(message=_("You have accepted the friendship request from %(from_user)s") % {'from_user': invitation.from_user})
                            is_friend = True
                            other_friends = Friendship.objects.friends_for_user(other_user)
                    except FriendshipInvitation.DoesNotExist:
                        pass
        else:
            invite_form = InviteFriendForm(request.user, {
                'to_user': username,
                'message': ugettext("Let's be friends!"),
            })
    previous_invitations_to = FriendshipInvitation.objects.filter(to_user=other_user, from_user=request.user)
    previous_invitations_from = FriendshipInvitation.objects.filter(to_user=request.user, from_user=other_user)
    
    profile_form = None
    extended_form = None
    if is_me:
        baseprofile = other_user.get_profile()
        extended_profile = None
        if hasattr(baseprofile, 'get_extended_profile'):
            extended_profile = baseprofile.get_extended_profile()
        if request.method == "POST":
            if request.POST["action"] == "update":
                profile_form = ProfileForm(request.POST, instance=baseprofile)
                if profile_form.is_valid():
                    profile = profile_form.save(commit=False)
                    profile.user = other_user
                    profile.save()               
            else:
                if extended_profile:
                    extended_form = baseprofile.get_extended_profile_form()(instance=extended_profile)
                profile_form = ProfileForm(instance=baseprofile)
        else:
            if extended_profile:
                extended_form = baseprofile.get_extended_profile_form()(instance=extended_profile)
            profile_form = ProfileForm(instance=baseprofile)

    participated = None
    return render_to_response(template_name, {
        "profile_form": profile_form,
        "extended_form": extended_form,
        "is_me": is_me,
        "participated": participated,
        "unread_messages_num": other_user.received_messages.filter(read_at__isnull=True).count(),
        #"friendship_requests_num": other_user.invitations_to.filter(status__in=[1,2]).count(),
        "is_friend": is_friend,
        "other_user": other_user,
        "other_friends": other_friends,
        "invite_form": invite_form,
        "previous_invitations_to": previous_invitations_to,
        "previous_invitations_from": previous_invitations_from,
    }, context_instance=RequestContext(request))

def friend_request(request, username, template_name="profiles/friend_request.html"):
    invite_form = InviteFriendForm(request.user, {
        'to_user': username,
        'other_user': request.user,
        'message': ugettext("Let's be friends!"),
    })
    
    return render_to_response(template_name, {
        "invite_form": invite_form,
    }, context_instance=RequestContext(request))

def username_autocomplete_friends(request):
    if request.user.is_authenticated():
        q = request.GET.get("q")
        friends = Friendship.objects.friends_for_user(request.user)
        content = []
        for friendship in friends:
            if friendship["friend"].username.lower().startswith(q):
                try:
                    profile = friendship["friend"].get_profile()
                    entry = "%s,,%s,,%s" % (
                        avatar(friendship["friend"], 40),
                        friendship["friend"].username,
                        profile.location
                    )
                except Profile.DoesNotExist:
                    pass
                content.append(entry)
        response = HttpResponse("\n".join(content))
    else:
        response = HttpResponseForbidden()
    setattr(response, "djangologging.suppress_output", True)
    return response

def username_autocomplete(request, template_name="account/username_autocomplete.html"):
    from django.contrib.auth.models import User
    users = User.objects.filter(username__istartswith=request.GET["q"]).exclude(username__exact=request.user.username)
    content = []
    for user in users:
        try:
            #profile = user.get_profile()
            entry = "%s,,%s,,%s" % (
                avatar(user, 40),
                user.username,
                user.username
            )
        except Profile.DoesNotExist:
            pass

        content.append(entry)
    response = HttpResponse("\n".join(content))
    setattr(response, "djangologging.suppress_output", True)
    return response



def change_email(request, template_name="profiles/change_email.html"):
    if request.user:
        if request.POST:
            user = request.user
            if request.POST.get("email", False):
                user.email = request.POST.get("email")
                user.save()
                return render_to_response(template_name,
                    {'user': request.user, "saved": True},
                    context_instance = RequestContext(request),
                )
        else:
            return render_to_response(template_name,
                {'user': request.user},
                context_instance = RequestContext(request),
            )
    else:
        return render_to_response('error.html',
            {'title': "Nicht erlaubt", "text": u"Sie sind nicht eingelogged."},
            context_instance = RequestContext(request),
        )