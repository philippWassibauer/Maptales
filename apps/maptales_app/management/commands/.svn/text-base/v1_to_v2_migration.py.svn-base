from django.core.management.base import NoArgsCommand
from django.conf import settings
import os

from avatar.models import Avatar
from avatar import AUTO_GENERATE_AVATAR_SIZES
from django.db import connection
import psycopg2
import psycopg2.extras as pe
import time
import sys
import re

from video.models import Video
from activity_stream.models import ActivityFollower
from avatar.models import Avatar, avatar_file_path
from django.contrib.auth.models import User
from profiles.models import Profile
from account.models import Account
from maptales_app.models import MigratedItem
from story.models import StoryLineItem, StoryLineItemMedia, Story
from photos.models import Image
from geo.models import GeoLineTag, GeoPointTag, MGPXTrack, MGPXTrackSegment, MAPSTYLE_SATELLITE, MAPSTYLE_HYBRID, MAPSTYLE_MAP
from django.core.files.base import ContentFile
from maptales_app.models import PRIVACY_PRIVATE, PRIVACY_PUBLIC, PRIVACY_FRIENDS
from django.contrib.gis.geos import LineString, Point
from django.db import transaction
import datetime
from django.template.defaultfilters import slugify
from misc.utils import make_unique
from tagging.models import Tag
from hitcount.models import HitCount

conn = psycopg2.connect (host = "localhost",
                           user = "maptales",
                           password = "kleini",
                           database = "maptales")

path_to_images = "/Users/phil/Documents/original/"
path_to_profileimages = "/Users/phil/Documents/48/"

class Command(NoArgsCommand):
    help = "Migrates the db form v1 to v2"
    
    
    def handle_noargs(self, **options):
        normalize_dates()
        
        users = get_users(200000)
        # loop through the users and save them
        for user in users:
            was_stored = MigratedItem.objects.filter(type="user", old_id=user["user_id"]).count()
            if was_stored:
                print "USER: %s was stored already!"%user["user_id"]
            else:
                stored_user = store_user(user)
              
              
        # contacts
        contacts = get_contacts()
        for contact in contacts:
            try:
                from_user = User.objects.get(pk=get_new_id("user", contact["user_id"]))
                to_user = User.objects.get(pk=get_new_id("user", contact["contact"]))
            
                following = ActivityFollower(to_user=to_user, from_user=from_user)
                following.save()
                
                follower = ActivityFollower(to_user=from_user, from_user=to_user)
                follower.save()
                
                migrated_contact = MigratedItem(type="contact", old_id=contact["contact"],
                                     new_id=following.pk)
                migrated_contact.save()
            except:
                print "Could not make activity follower"
        
        for user in User.objects.all():
            p = re.compile( '([^a-zA-Z_0-9])')
            oldname = user.username
            user.username = p.sub("_", oldname)
            user.save()
            print "Replaced username: %s with username: %s"%(oldname,user.username)
   
   

def make_avatar(old_user):
    if old_user["profileicon"]:
        icon = path_to_profileimages+old_user["profileicon"]
        user = User.objects.get(pk=get_new_id("user", old_user["user_id"]))
        path = avatar_file_path(user=user, filename=old_user["profileicon"])
        avatar = Avatar(
            user = user,
            primary = True,
            avatar = path,
        )
        new_file = avatar.avatar.storage.save(path, ContentFile(open(icon, "r").read()))
        avatar.save()
    
    
def get_old_id(type, new_id):
    try:
        return MigratedItem.objects.get(type=type, new_id=new_id).old_id
    except:
        print "Cant find: %s.%s"%(type, new_id)


def get_new_id(type, old_id):
    try:
        return MigratedItem.objects.get(type=type, old_id=int(old_id)).new_id
    except:
        print "Cant find: %s.%s"%(type, old_id)
    

def convert_time(timestring):
    if not timestring:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    if type(timestring) == datetime.datetime:
        timestring = timestring.strftime("%Y-%m-%d %H:%M:%S")
        
    if timestring.rfind("."):
        timestring=timestring[0:timestring.rfind(".")]
    return timestring

def get_privacy_of_old_privacy(privacy):
    if privacy == 0:
        return PRIVACY_PRIVATE
    elif privacy == 1:
        return PRIVACY_PUBLIC
    elif privacy == 2:
        return PRIVACY_FRIENDS
    
    
def get_status_of_old_privacy(privacy):
    if privacy == 0:
        return Story.STATUS_DRAFT
    elif privacy == 1:
        return Story.STATUS_PUBLIC
    else:
        return Story.STATUS_DRAFT

def convert_mapmode(mapmode):
    if mapmode == 0:
        return MAPSTYLE_SATELLITE
    elif mapmode == 1:
        return MAPSTYLE_MAP
    elif mapmode == 2:
        return MAPSTYLE_HYBRID


def get_mapobject_of_id(id):
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""SELECT *
                        FROM medias m
                        where m.media_id = %s"""%(id,))
    media_item = cursor.fetchone()
    
    cursor.execute ("""SELECT *
                        FROM markers m, mapobjects mo
                        where mo.mapobject_id = m.marker_id
                        and mo.mapobject_id = %s"""%(media_item['mapobject_id'],))
    return cursor.fetchone()

def get_marker(id):
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""SELECT *
                        FROM markers m, mapobjects mo
                        where mo.mapobject_id = m.marker_id
                        and mo.mapobject_id = %s"""%(id,))
    return cursor.fetchone()
    
def get_users(number):
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""SELECT *
                        FROM users u order by user_id asc limit %s"""%number)
    return cursor.fetchall()


def get_tags():
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""SELECT *
                        FROM tags u""")
    return cursor.fetchall()
    
def get_tags_of_item(id):
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""select t.tag from userobject_tag ut, tags t
                        where ut.tag_id = t.tag_id and ut.userobject_id = %s"""%id)
    return cursor.fetchall()
    
    
def store_tags_of_item(content_object, old_id):
    tags = get_tags_of_item(old_id)
    if tags:
        print "Storing tags of item %s"%str(content_object)
        tag_array = [t["tag"] for t in tags]
        print "Tags: %s"%", ".join(tag_array)
        Tag.objects.update_tags(content_object, " ".join(tag_array))
        

def set_hit_count(content_object, count):
    print "Storing hitcount of item %s : %s"%(str(content_object), count)
    hitcount = HitCount(content_object=content_object, hits=count)
    hitcount.save()
    
def get_stories(userid):
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""select * from stories s, userobjects uo
                            where uo.creator_id = %s
                                and s.story_id = uo.userobject_id
                                """%(userid,)) # and LENGTH(p.text) > 0 
    return cursor.fetchall()
    
    
def get_posts(userid):
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""select * from posts p, userobjects uo, medias m
                            where uo.creator_id = %s
                                and p.post_id = uo.userobject_id
                                and m.media_id = p.post_id
                                and m.mapobject_id is null
                                """%(userid,)) # and LENGTH(p.text) > 0
    first_batch = cursor.fetchall()
    first_count = len(first_batch)
    
    cursor.execute ("""select * from posts p, userobjects uo, medias m
                            where uo.creator_id = %s
                                and p.post_id = uo.userobject_id
                                and m.media_id = p.post_id
                                and m.mapobject_id is not null
                                and m.mapobject_id not in
                                (Select l2.line_id from lines l2, userobjects uo2
                                    where l2.line_id = uo2.userobject_id
                                        and uo2.creator_id=%s)
                                """%(userid,userid))
    
    placed = cursor.fetchall()
    second_batch_count = len(placed)
    first_batch.extend(placed)
    print "placed: %s unplaced: %s final: %s "%(first_count, second_batch_count, len(first_batch) )
    return first_batch


def get_post_of_line(line_id):
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""select * from posts p, userobjects uo, medias m
                            where m.mapobject_id = %s
                                and p.post_id = uo.userobject_id
                                and m.media_id = p.post_id
                                """%(line_id,)) # and LENGTH(p.text) > 0 
    return cursor.fetchone()
    
    
def get_images(userid):
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""select * from images i, userobjects uo, medias m
                            where uo.creator_id = %s
                                and i.image_id = uo.userobject_id
                                and m.media_id = i.image_id
                                order by m.timestamp asc, i.image_id asc
                                """%(userid,))
    try:
        return cursor.fetchall()
    except:
        print """Error running: select * from images i, userobjects uo, medias m
                            where uo.creator_id = %s
                                and i.image_id = uo.userobject_id
                                and m.media_id = i.image_id
                               """%(userid,)


def get_lines(userid):
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""select * from lines l, mapobjects mo, userobjects uo
                            where uo.creator_id = %s
                                and l.line_id = uo.userobject_id
                                and mo.mapobject_id = uo.userobject_id"""%(userid,))
    return cursor.fetchall()

def get_story_of_line(lineid):
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""select * from lines l, medias m
                            where l.line_id = %s
                                and m.mapobject_id = l.line_id"""%(lineid,))
    return cursor.fetchone()
    

def get_contacts():
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""select * from contacts c""")
    return cursor.fetchall()

def get_videos(userid):
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""select * from videos v, userobjects uo, medias m
                            where uo.creator_id = %s
                                and v.video_id = uo.userobject_id
                                and m.media_id = v.video_id"""%(userid,))
    return cursor.fetchall()
    
    
def get_photos_with_story():
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""select * from images i, medias m
                            where m.story_id is not null
                                and m.media_id = i.image_id
                                and i.secret is null""")
    return cursor.fetchall()
    
def get_videos_with_story(story_id):
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""select * from videos v, medias m
                            where m.story_id is not null
                                and m.media_id = v.video_id""")
    return cursor.fetchall()
    

def normalize_dates():
    cursor = conn.cursor (cursor_factory=pe.DictCursor)
    cursor.execute ("""update medias set timestamp = '1976-01-01 00:00:00'
                            where timestamp < '1976-01-01 00:00:00'""")
   

def geotag_item(old_id, item, user):
    mapobject = get_mapobject_of_id(old_id)
    if mapobject and mapobject['location']:
        location = make_point_of_string(mapobject['location'])
        # geotagging
        geopointtag = GeoPointTag(content_object=item,
                                        location=location,
                                        creator=user)
        geopointtag.save()
    
    
    
    
    
    
def make_point_of_string(pointstring):
    pointstring = pointstring.replace("(", "").replace(")", "")
    pointarray = pointstring.split(",")
    return Point(float(pointarray[0]), float(pointarray[1]))

def make_linestring_of_string(linestring, start_marker, end_marker):

    pointstring = linestring[2:-2]
    pointarray = pointstring.split("),(")
    final_array = []
    if start_marker:
        marker = get_marker(start_marker)
        if marker:
            point = make_point_of_string(marker['location'])
            final_array.append((point.x, point.y))
        
    for item in pointarray:
        itemarray = item.split(",")
        final_array.append((float(itemarray[0]), float(itemarray[1])))
    
    if end_marker:
        marker = get_marker(end_marker)
        if marker:
            point = make_point_of_string(marker['location'])
            final_array.append((point.x, point.y))
            
    print "Length: "+str(len(final_array))
    if len(final_array)<3:
        return None
    
    return LineString(final_array)
    

@transaction.commit_on_success
def store_user(data):
    
    #
    # User
    #
    firstname = data['firstname']
    if not firstname:
        firstname = " "
    lastname = data['lastname']
    if not lastname:
        lastname = " "
    user = User(username=data['name'], first_name=firstname,
                last_name=lastname, email=data['email'], password="md5$$"+data["pass"])
    user.save(force_insert=True)
    
    print "User: "+data['name']
    
    
    city = data['city']
    if not city:
        city = " "
        
    #profile = Profile(user=user,
    #                    first_name=firstname,
    #                    last_name=lastname,
    #                    city=city,
    #                    about=data['description'])
    #profile.save()
    #account = Account(user=user)
    #account.save()
    
    # avatar
    
    #
    # stories - do them first, since they are containers that we want to add items to
    #
    stories = get_stories(data["user_id"])
    for story in stories:
        print "-Story: "+str(story['story_id'])
        title = story['title']
        if not title:
            title = " "
            
        new_story = Story(title=title,
                          slug=slugify(title),
                      creator=user,
                      description=story['text'],
                      mapmode=convert_mapmode(story['mapmode']),
                      creation_date=convert_time(story['timestamp']),
                      update_date=convert_time(story['timestamp']),
                      privacy=get_privacy_of_old_privacy(story['right_view']),
                      status=get_status_of_old_privacy(story['right_view']))
        
        new_story.slug = make_unique(new_story, lambda x: Story.objects.filter(slug__exact=x.slug).count() == 0)
        
        new_story.save()
        migrated_post = MigratedItem(type="story", old_id=story["story_id"],
                                 new_id=new_story.pk)
        migrated_post.save()
        
        store_tags_of_item(new_story, story['story_id'])
        
        set_hit_count(new_story, story['view_count'])
    
    
    
    
    # lines
    lines = get_lines(data["user_id"])
    if lines:
        for line in lines:
            print "-Line: "+str(line['line_id'])
            linestring = make_linestring_of_string(line["controlpoints"], line["start_marker_id"], line["end_marker_id"])
            if linestring:
                line_post = get_post_of_line(line['line_id'])
                if not line_post:
                    title = " "
                    description = " "
                else:
                    if line_post['title']:
                        title = line_post['title']
                    else:
                        title = " "
                    
                    if line_post['text']:
                        description = line_post['text']
                    else:
                        description = " "
                    
                new_line = GeoLineTag(creator=user,
                                title=title,
                                description=description,
                                line=linestring,
                                )
                
                # add to story
                line_w_story = get_story_of_line(line['line_id'])
                if line_w_story and line_w_story['story_id']:
                    try:
                        new_story = Story.objects.get(pk=get_new_id("story",line_w_story['story_id']))
                        print "Adding line %s (%s) to story %s (%s)"%(line['line_id'], new_line.id, line_w_story['story_id'], new_story.id)
                        new_line.content_object = new_story
                    except:
                        print "Could not add Story"
                    
                new_line.save()
                migrated_line = MigratedItem(type="line", old_id=line["line_id"],
                                         new_id=new_line.pk)
                migrated_line.save()
            
                
    
    
    # video
    videos = get_videos(data["user_id"])
    for video in videos:
        print "-Video: "+str(video['video_id'])
        if video['medialocation']:
            import re
            video_id = re.findall(r"/v/(.+)", video['medialocation'])[0]
            import_url = "http://www.youtube.com/watch?v="+video_id
            comment = video['text']
            if not comment:
                comment = " "
                
            new_video = Video(creator=user,
                            title=video['title'],
                            comment=comment,
                            was_uploaded=False,
                            import_url=import_url,
                            thumbnail_url=video['thumb1'],
                            safetylevel=get_privacy_of_old_privacy(video['right_view']),
                            last_modified=convert_time(video['timestamp']),
                            date_added=convert_time(video['timestamp']),
                            )
            new_video.save()
            migrated_video = MigratedItem(type="video", old_id=video["video_id"],
                                     new_id=new_video.pk)
            migrated_video.save()
            
            # add to story
            if video["story_id"]:
                story = Story.objects.get(pk=get_new_id("story", video["story_id"]))
                
                count = StoryLineItem.objects.filter(creator=user, story=story, timestamp_start__lte=convert_time(video['timestamp'])).count()
                print "Adding video %s (%s) to story %s (%s) at position: %s "%(video['video_id'], new_video.id, video["story_id"], story.id, count)
                
                text = video['text']
                if not text:
                    text = " "
                    
                story_line_item = StoryLineItem(creator=user, story=story, text=text,
                                         timestamp_start=convert_time(video['timestamp']), timestamp_end=convert_time(video['timestamp']))
                story_line_item.save()
                story_line_item_media = StoryLineItemMedia(storylineitem=story_line_item, content_object=new_video)
                story_line_item_media.save()
                
                # geotag
                if video['mapobject_id']:
                    geotag_item(video["video_id"], story_line_item, user)
            
            if video['mapobject_id']:
                geotag_item(video["video_id"], new_video, user)
        
            store_tags_of_item(new_video, video["video_id"])
            set_hit_count(new_video, video['view_count'])
            
    # posts
    posts = get_posts(data["user_id"])
    for post in posts:
        print "-Post: "+str(post['post_id'])
        if post['story_id']:
            post_text = post['text']
            if not post_text:
                post_text = " "
            
            try:
                post_story = Story.objects.get(pk=get_new_id("story", post['story_id']))
                count = StoryLineItem.objects.filter(creator=user, story=story, timestamp_start__lte=convert_time(post['timestamp'])).count()
                print "Adding post %s to story %s (%s) at position: %s "%(post['post_id'], post["story_id"], post_story.id, count)
                new_post = StoryLineItem(creator=user, story=post_story, text=post_text,
                                         timestamp_start=convert_time(post['timestamp']),
                                         timestamp_end=convert_time(post['timestamp']))
                new_post.save()
                migrated_post = MigratedItem(type="post", old_id=post["post_id"],
                                         new_id=new_post.pk)
                migrated_post.save()
            
                if post['mapobject_id']:
                    geotag_item(post["post_id"], new_post, user)
                    
                store_tags_of_item(new_post, post["post_id"])
                set_hit_count(new_post, post['view_count'])
            except:
                print "Could not add to Story"
    
    
    # images
    images = get_images(data["user_id"])
    if images:
        for image in images:
            print "-Image: "+str(image['image_id'])
            caption = image['text']
            if not caption:
                caption = " "
            
            title = image['title']
            if not title:
                title = " "
                
            new_image = Image(member=user,
                            title=title,
                            caption=caption,
                            date_added=convert_time(image['timestamp']),
                            )
            
            
            try:
                new_image.image.save(os.path.basename(image["filename"]+".jpg"), ContentFile(open(path_to_images+image["filename"]+".jpg", "r").read()))
                migrated_image = MigratedItem(type="image", old_id=image["image_id"],
                                         new_id=new_image.pk)
                new_image.save()
                migrated_image.save()
                
                if image["story_id"]:
                    story = Story.objects.get(pk=get_new_id("story", image["story_id"]))
                    count = StoryLineItem.objects.filter(creator=user, story=story, timestamp_start__lte=convert_time(image['timestamp'])).count()
                    print "Adding image %s (%s) to story %s (%s) at position: %s "%(image['image_id'], new_image.id, image["story_id"], story.id, count)
                    story_line_item = StoryLineItem(creator=user, story=story, text=caption,
                                             position=count,
                                             timestamp_start=convert_time(image['timestamp']),
                                             timestamp_end=convert_time(image['timestamp']))
                    story_line_item.save()
                    story_line_item_media = StoryLineItemMedia(storylineitem=story_line_item, content_object=new_image)
                    story_line_item_media.save()
                    
                    if image['mapobject_id']:
                        geotag_item(image['image_id'], story_line_item, user)
            
                if image['mapobject_id']:
                    geotag_item(image['image_id'], new_image, user)
                    
                store_tags_of_item(new_image, image["image_id"])
                set_hit_count(new_image, image['view_count'])
            except:
                print "Could not store image: %s filename: %s"%(image['image_id'], image['filename'])
                
    # story image
    
    
    # store user
    migrated_user = MigratedItem(type="user", old_id=data["user_id"],
                                 new_id=user.pk)
    migrated_user.save()
    make_avatar(data)
    
    # flickr images
    # TODO:
    