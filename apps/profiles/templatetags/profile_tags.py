from django import template
from activity_stream.models import get_people_i_follow
from native_tags.decorators import function, comparison, filter
from friends.forms import Friendship
from friends.models import FriendshipInvitation
from django.template.loader import render_to_string

register = template.Library()

def show_profile_preview(user):
    return {"user": user}
register.inclusion_tag("profiles/profile_preview_horizontal.html")(show_profile_preview)


def show_profile_header(viewed_user, user, title=""):
    return {"viewed_user": viewed_user, "user":user, "title":title}
register.inclusion_tag("profiles/profile_header.html")(show_profile_header)


def count_of_votes(viewed_user):
    from voting.models import Vote
    return Vote.objects.filter(user=viewed_user).count()
count_of_votes = function(count_of_votes)


def show_contact_select(viewed_user, element_id, callback, count=20):
    users = get_people_i_follow(viewed_user, count)
    return {"viewed_user":viewed_user,
            "element_id": element_id,
            "callback": callback,
            "count": count,
            "users": users}
register.inclusion_tag("profiles/show_contact_select.html")(show_contact_select)


def are_friends(user, user2):
    if user.is_authenticated():
        are_friend = Friendship.objects.are_friends(user, user2)
        return are_friend
    else:
        return False
are_friends = comparison(are_friends)



def received_friendship_request_from_user(user, from_user):
    if from_user.is_authenticated():
        are_friend = FriendshipInvitation.objects.invitations(to_user=user,
                                                              from_user=from_user)
        return are_friend
    return False
received_friendship_request_from_user = comparison(received_friendship_request_from_user)


def sent_friendship_request_to_user(user, to_user):
    if to_user.is_authenticated():
        are_friend = FriendshipInvitation.objects.invitations(to_user=to_user,
                                                              from_user=user)
        return are_friend
    return False
sent_friendship_request_to_user = comparison(sent_friendship_request_to_user)


def friends_of_user(user, count=20, template_name="friends_app/friends_list.html"):
    friends = Friendship.objects.friends_for_user(user)[0:count]
    return render_to_string(template_name, {
        "friends": friends,
    })
friends_of_user = function(friends_of_user)
