from threadedcomments.models import ThreadedComment
from django.db.models.signals import post_save
from activity_stream.models import create_activity_item, ActivityStreamItem
from django.contrib.gis.db import models
from brabeion import badges
from brabeion.base import Badge, BadgeAwarded
from django.contrib.auth.models import User

PRIVACY_PUBLIC = 1
PRIVACY_FRIENDS = 2
PRIVACY_PRIVATE = 3


PRIVACY_LEVELS = (
    (PRIVACY_PUBLIC, "Public"),
    (PRIVACY_FRIENDS, "Friends"),
    (PRIVACY_PRIVATE, "Private"),
)


class NewbieBadge(Badge):
    slug = "newbie"
    levels = [
        {"name":"Newbie", "description":"Signed Up"},
    ]
    events = [
        "registered",
    ]
    multiple = False
    
    def award(self, **state):
        user = state["user"]
        return BadgeAwarded(level=1)
badges.register(NewbieBadge)




class VeteranBadge(Badge):
    slug = "veteran"
    levels = [
        {"name":"Veteran", "description":"Signed Up in V1 of Maptales"},
    ]
    events = [
        "existing_account",
    ]
    multiple = False
    
    def award(self, **state):
        user = state["user"]
        return BadgeAwarded(level=1)
badges.register(VeteranBadge)


class FullEgoBadge(Badge):
    slug = "fullego"
    levels = [
        {"name":"FullEgo", "description":"Profile filled out"},
    ]
    events = [
        "profile_edited",
    ]
    multiple = False
    
    def award(self, **state):
        user = state["user"]
        profile = user.get_profile()
        if profile.is_filled_out():
            return BadgeAwarded(level=1)
        else:
            return None
badges.register(FullEgoBadge)


class GlobetrotterBadge(Badge):
    slug = "globetrotter"
    levels = [
        {"name":"Globetrotter Bronze", "description":"More then 3 Countries"},
        {"name":"Globetrotter Silver", "description":"More then 10 Countries"},
        {"name":"Globetrotter Gold", "description":"More then 50 Countries"}
    ]
    events = [
        "placed_item",
    ]
    
    multiple = False
    
    def award(self, **state):
        user = state["user"]
        profile = user.get_profile()
        if profile.is_filled_out():
            return BadgeAwarded(level=1)
        else:
            return None
badges.register(GlobetrotterBadge)


def registered(sender, instance=None, **kwargs):
    if instance is None:
        return
    badges.possibly_award_badge("registered", user=instance)
post_save.connect(registered, sender=User)


from brabeion.signals import badge_awarded
def badge_award(sender, badge, **kwargs):
    pass
    #TODO: THIS CAUSES ERRORS IN TESTS SINCE BADGE_AWARD IS NOT EXISTENT WHEN USERS GET CREATED
    #try:
    #    create_activity_item("badge_awarded", badge.user, badge)
    #except:
    #    pass
badge_awarded.connect(badge_award)

class PrivateBetaEmail(models.Model):
    email = models.CharField('Email', max_length=300)
    
class MigratedItem(models.Model):
    type = models.CharField('Type', max_length=200)
    old_id = models.IntegerField("Old Id")
    new_id = models.IntegerField("New Id")
    
    
class TourCities(models.Model):
    name = models.CharField('Name', max_length=200)
    location = models.PointField(srid=4326)
    zoom_level = models.IntegerField()
    slug = models.SlugField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
    
def posted_comment(sender, instance=None, **kwargs):
    if instance is None:
        return
    
    if not isinstance(instance.content_object, ActivityStreamItem):
        create_activity_item("posted_comment", instance.user, instance)

post_save.connect(posted_comment, sender=ThreadedComment)