
from south.db import db
from django.db import models
from geo.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'MGPXTrack.safetylevel'
        db.add_column('geo_mgpxtrack', 'safetylevel', orm['geo.mgpxtrack:safetylevel'])
        
        # Changing field 'GeoGeometryTag.created_at'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 11, 10, 12, 2, 44, 393306)))
        db.alter_column('geo_geogeometrytag', 'created_at', orm['geo.geogeometrytag:created_at'])
        
        # Changing field 'MGPXTrack.creation_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 11, 10, 12, 2, 44, 394072)))
        db.alter_column('geo_mgpxtrack', 'creation_date', orm['geo.mgpxtrack:creation_date'])
        
        # Changing field 'MGPXTrack.update_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 11, 10, 12, 2, 44, 394109)))
        db.alter_column('geo_mgpxtrack', 'update_date', orm['geo.mgpxtrack:update_date'])
        
        # Changing field 'MGPXTrackSegment.creation_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 11, 10, 12, 2, 44, 395255)))
        db.alter_column('geo_mgpxtracksegment', 'creation_date', orm['geo.mgpxtracksegment:creation_date'])
        
        # Changing field 'MGPXTrackSegment.update_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 11, 10, 12, 2, 44, 395285)))
        db.alter_column('geo_mgpxtracksegment', 'update_date', orm['geo.mgpxtracksegment:update_date'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'MGPXTrack.safetylevel'
        db.delete_column('geo_mgpxtrack', 'safetylevel')
        
        # Changing field 'GeoGeometryTag.created_at'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 11, 9, 19, 59, 32, 908786)))
        db.alter_column('geo_geogeometrytag', 'created_at', orm['geo.geogeometrytag:created_at'])
        
        # Changing field 'MGPXTrack.creation_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 11, 9, 19, 59, 32, 909516)))
        db.alter_column('geo_mgpxtrack', 'creation_date', orm['geo.mgpxtrack:creation_date'])
        
        # Changing field 'MGPXTrack.update_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 11, 9, 19, 59, 32, 909546)))
        db.alter_column('geo_mgpxtrack', 'update_date', orm['geo.mgpxtrack:update_date'])
        
        # Changing field 'MGPXTrackSegment.creation_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 11, 9, 19, 59, 32, 910621)))
        db.alter_column('geo_mgpxtracksegment', 'creation_date', orm['geo.mgpxtracksegment:creation_date'])
        
        # Changing field 'MGPXTrackSegment.update_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 11, 9, 19, 59, 32, 910651)))
        db.alter_column('geo_mgpxtracksegment', 'update_date', orm['geo.mgpxtracksegment:update_date'])
        
    
    
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
        'geo.geogeometrytag': {
            'Meta': {'unique_together': "(('content_type', 'object_id'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 11, 10, 12, 2, 44, 393306)'}),
            'geometry_collection': ('django.contrib.gis.db.models.fields.GeometryCollectionField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'geo.mgpxtrack': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 11, 10, 12, 2, 44, 394072)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gps_tracks'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'distance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'from_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'safetylevel': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'to_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 11, 10, 12, 2, 44, 394109)'})
        },
        'geo.mgpxtracksegment': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 11, 10, 12, 2, 44, 395255)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gps_track_segments'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'distance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'from_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'gpx_height_graph': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'segments'", 'null': 'True', 'to': "orm['geo.MGPXTrack']"}),
            'raw_track': ('SerializedDataField', ["_('raw_track')"], {'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'to_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'track': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 11, 10, 12, 2, 44, 395285)'})
        }
    }
    
    complete_apps = ['geo']
