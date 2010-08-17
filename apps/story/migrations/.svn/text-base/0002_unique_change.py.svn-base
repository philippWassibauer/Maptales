
from south.db import db
from django.db import models
from story.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Deleting unique_together for [content_type, object_id] on storylineitem.
        db.delete_unique('story_storylineitem', ['content_type_id', 'object_id'])
        
        # Creating unique_together for [content_type, object_id, story] on StoryLineItem.
        db.create_unique('story_storylineitem', ['content_type_id', 'object_id', 'story_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [content_type, object_id, story] on StoryLineItem.
        db.delete_unique('story_storylineitem', ['content_type_id', 'object_id', 'story_id'])
        
        # Creating unique_together for [content_type, object_id] on storylineitem.
        db.create_unique('story_storylineitem', ['content_type_id', 'object_id'])
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'geo.mgpxtrack': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 11, 11, 15, 17, 26, 684457)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gps_tracks'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'distance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'from_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'safetylevel': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'to_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 11, 11, 15, 17, 26, 684511)'})
        },
        'photologue.photoeffect': {
            'background_color': ('django.db.models.fields.CharField', [], {'default': "'#FFFFFF'", 'max_length': '7'}),
            'brightness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'color': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'contrast': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'reflection_size': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'reflection_strength': ('django.db.models.fields.FloatField', [], {'default': '0.59999999999999998'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'transpose_method': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        'story.story': {
            'creation_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2009, 11, 11, 15, 17, 26, 783753)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'from_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapmode': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'privacy': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '300', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'to_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'tracks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['geo.MGPXTrack']", 'null': 'True', 'blank': 'True'}),
            'update_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2009, 11, 11, 15, 17, 26, 783793)'})
        },
        'story.storyimage': {
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'storyimage_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'story': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'storyimage'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['story.Story']"}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'story.storylineitem': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'story'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'position': ('PositionField', [], {'unique_for_field': "'story'"}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'storyline'", 'to': "orm['story.Story']"})
        }
    }
    
    complete_apps = ['story']
