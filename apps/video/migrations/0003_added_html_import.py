
from south.db import db
from django.db import models
from video.models import *

class Migration:
    
    def forwards(self, orm):
        db.add_column('video_video', 'html_code', orm['video.video:html_code'])
        db.add_column('video_video', 'from_html_code', orm['video.video:from_html_code'])
        # Changing field 'Video.date_added'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 11, 21, 15, 24, 52, 951152), auto_now_add=True, blank=True))
        db.alter_column('video_video', 'date_added', orm['video.video:date_added'])
        
    
    
    def backwards(self, orm):
        pass
        # Changing field 'Video.date_added'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 11, 21, 15, 24, 44, 874993), auto_now_add=True, blank=True))
        #db.alter_column('video_video', 'date_added', orm['video.video:date_added'])
        #db.add_column('video_video', 'html_code', orm['video.video:html_code'])
        #db.add_column('video_video', 'from_html_code', orm['video.video:from_html_code'])
    
    
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
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 11, 21, 15, 24, 52, 951152)', 'auto_now_add': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'from_html_code': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'html_code': ('django.db.models.fields.TextField', [], {'max_length': '850', 'blank': 'True'}),
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
