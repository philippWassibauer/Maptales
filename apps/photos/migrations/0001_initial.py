
from south.db import db
from django.db import models
from photos.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'PhotoSet'
        db.create_table('photos_photoset', (
            ('id', orm['photos.PhotoSet:id']),
            ('name', orm['photos.PhotoSet:name']),
            ('description', orm['photos.PhotoSet:description']),
            ('publish_type', orm['photos.PhotoSet:publish_type']),
            ('tags', orm['photos.PhotoSet:tags']),
        ))
        db.send_create_signal('photos', ['PhotoSet'])
        
        # Adding model 'Pool'
        db.create_table('photos_pool', (
            ('id', orm['photos.Pool:id']),
            ('photo', orm['photos.Pool:photo']),
            ('content_type', orm['photos.Pool:content_type']),
            ('object_id', orm['photos.Pool:object_id']),
            ('created_at', orm['photos.Pool:created_at']),
        ))
        db.send_create_signal('photos', ['Pool'])
        
        # Adding model 'Image'
        db.create_table('photos_image', (
            ('id', orm['photos.Image:id']),
            ('image', orm['photos.Image:image']),
            ('date_taken', orm['photos.Image:date_taken']),
            ('view_count', orm['photos.Image:view_count']),
            ('crop_from', orm['photos.Image:crop_from']),
            ('effect', orm['photos.Image:effect']),
            ('title', orm['photos.Image:title']),
            ('title_slug', orm['photos.Image:title_slug']),
            ('caption', orm['photos.Image:caption']),
            ('date_added', orm['photos.Image:date_added']),
            ('is_public', orm['photos.Image:is_public']),
            ('member', orm['photos.Image:member']),
            ('safetylevel', orm['photos.Image:safetylevel']),
            ('tags', orm['photos.Image:tags']),
            ('location', orm['photos.Image:location']),
            ('location_name', orm['photos.Image:location_name']),
        ))
        db.send_create_signal('photos', ['Image'])
        
        # Adding ManyToManyField 'Image.photoset'
        db.create_table('photos_image_photoset', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('image', models.ForeignKey(orm.Image, null=False)),
            ('photoset', models.ForeignKey(orm.PhotoSet, null=False))
        ))
        
        # Creating unique_together for [photo, content_type, object_id] on Pool.
        db.create_unique('photos_pool', ['photo_id', 'content_type_id', 'object_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [photo, content_type, object_id] on Pool.
        db.delete_unique('photos_pool', ['photo_id', 'content_type_id', 'object_id'])
        
        # Deleting model 'PhotoSet'
        db.delete_table('photos_photoset')
        
        # Deleting model 'Pool'
        db.delete_table('photos_pool')
        
        # Deleting model 'Image'
        db.delete_table('photos_image')
        
        # Dropping ManyToManyField 'Image.photoset'
        db.delete_table('photos_image_photoset')
        
    
    
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
        'photos.image': {
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'image_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'added_photos'", 'null': 'True', 'to': "orm['auth.User']"}),
            'photoset': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['photos.PhotoSet']"}),
            'safetylevel': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tags': ('TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'photos.photoset': {
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'publish_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tags': ('TagField', [], {})
        },
        'photos.pool': {
            'Meta': {'unique_together': "(('photo', 'content_type', 'object_id'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['photos.Image']"})
        }
    }
    
    complete_apps = ['photos']
