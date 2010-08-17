
from south.db import db
from django.db import models
from video.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'VimeoToken'
        db.create_table('video_vimeotoken', (
            ('id', orm['video.VimeoToken:id']),
            ('name', orm['video.VimeoToken:name']),
            ('token', orm['video.VimeoToken:token']),
        ))
        db.send_create_signal('video', ['VimeoToken'])
        
        # Adding model 'Video'
        db.create_table('video_video', (
            ('id', orm['video.Video:id']),
            ('title', orm['video.Video:title']),
            ('comment', orm['video.Video:comment']),
            ('creator', orm['video.Video:creator']),
            ('was_uploaded', orm['video.Video:was_uploaded']),
            ('is_viewable', orm['video.Video:is_viewable']),
            ('import_url', orm['video.Video:import_url']),
            ('thumbnail_url', orm['video.Video:thumbnail_url']),
            ('external_id', orm['video.Video:external_id']),
            ('original_file', orm['video.Video:original_file']),
            ('tags', orm['video.Video:tags']),
            ('ticket_id', orm['video.Video:ticket_id']),
            ('safetylevel', orm['video.Video:safetylevel']),
            ('last_modified', orm['video.Video:last_modified']),
            ('date_added', orm['video.Video:date_added']),
        ))
        db.send_create_signal('video', ['Video'])
        
        # Adding model 'VideoPool'
        db.create_table('video_videopool', (
            ('id', orm['video.VideoPool:id']),
            ('video', orm['video.VideoPool:video']),
            ('content_type', orm['video.VideoPool:content_type']),
            ('object_id', orm['video.VideoPool:object_id']),
            ('created_at', orm['video.VideoPool:created_at']),
        ))
        db.send_create_signal('video', ['VideoPool'])
        
        # Creating unique_together for [video, content_type, object_id] on VideoPool.
        db.create_unique('video_videopool', ['video_id', 'content_type_id', 'object_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [video, content_type, object_id] on VideoPool.
        db.delete_unique('video_videopool', ['video_id', 'content_type_id', 'object_id'])
        
        # Deleting model 'VimeoToken'
        db.delete_table('video_vimeotoken')
        
        # Deleting model 'Video'
        db.delete_table('video_video')
        
        # Deleting model 'VideoPool'
        db.delete_table('video_videopool')
        
    
    
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
        'video.video': {
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added_videos'", 'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 10, 24, 10, 2, 30, 697401)', 'auto_now_add': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_url': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'is_viewable': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'original_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'safetylevel': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tags': ('TagField', [], {}),
            'thumbnail_url': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'ticket_id': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'was_uploaded': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'video.videopool': {
            'Meta': {'unique_together': "(('video', 'content_type', 'object_id'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"})
        },
        'video.vimeotoken': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }
    
    complete_apps = ['video']
