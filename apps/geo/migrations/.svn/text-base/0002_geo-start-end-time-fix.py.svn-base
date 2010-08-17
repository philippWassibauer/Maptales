
from south.db import db
from django.db import models
from geo.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'GeoGeometryTag.created_at'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 10, 24, 22, 17, 34, 770012)))
        db.alter_column('geo_geogeometrytag', 'created_at', orm['geo.geogeometrytag:created_at'])
        
        # Changing field 'MGPXTrack.start_time'
        # (to signature: django.db.models.fields.DateTimeField(null=True, blank=True))
        db.alter_column('geo_mgpxtrack', 'start_time', orm['geo.mgpxtrack:start_time'])
        
        # Changing field 'MGPXTrack.creation_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 10, 24, 22, 17, 34, 770996)))
        db.alter_column('geo_mgpxtrack', 'creation_date', orm['geo.mgpxtrack:creation_date'])
        
        # Changing field 'MGPXTrack.end_time'
        # (to signature: django.db.models.fields.DateTimeField(null=True, blank=True))
        db.alter_column('geo_mgpxtrack', 'end_time', orm['geo.mgpxtrack:end_time'])
        
        # Changing field 'MGPXTrack.update_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 10, 24, 22, 17, 34, 771036)))
        db.alter_column('geo_mgpxtrack', 'update_date', orm['geo.mgpxtrack:update_date'])
        
        # Changing field 'MGPXTrackSegment.start_time'
        # (to signature: django.db.models.fields.DateTimeField(null=True, blank=True))
        db.alter_column('geo_mgpxtracksegment', 'start_time', orm['geo.mgpxtracksegment:start_time'])
        
        # Changing field 'MGPXTrackSegment.creation_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 10, 24, 22, 17, 34, 771910)))
        db.alter_column('geo_mgpxtracksegment', 'creation_date', orm['geo.mgpxtracksegment:creation_date'])
        
        # Changing field 'MGPXTrackSegment.end_time'
        # (to signature: django.db.models.fields.DateTimeField(null=True, blank=True))
        db.alter_column('geo_mgpxtracksegment', 'end_time', orm['geo.mgpxtracksegment:end_time'])
        
        # Changing field 'MGPXTrackSegment.update_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime(2009, 10, 24, 22, 17, 34, 771945)))
        db.alter_column('geo_mgpxtracksegment', 'update_date', orm['geo.mgpxtracksegment:update_date'])
        
    
    
    def backwards(self, orm):
        
        # Changing field 'GeoGeometryTag.created_at'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime.now))
        db.alter_column('geo_geogeometrytag', 'created_at', orm['geo.geogeometrytag:created_at'])
        
        # Changing field 'MGPXTrack.start_time'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime.now))
        db.alter_column('geo_mgpxtrack', 'start_time', orm['geo.mgpxtrack:start_time'])
        
        # Changing field 'MGPXTrack.creation_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime.now))
        db.alter_column('geo_mgpxtrack', 'creation_date', orm['geo.mgpxtrack:creation_date'])
        
        # Changing field 'MGPXTrack.end_time'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime.now))
        db.alter_column('geo_mgpxtrack', 'end_time', orm['geo.mgpxtrack:end_time'])
        
        # Changing field 'MGPXTrack.update_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime.now))
        db.alter_column('geo_mgpxtrack', 'update_date', orm['geo.mgpxtrack:update_date'])
        
        # Changing field 'MGPXTrackSegment.start_time'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime.now))
        db.alter_column('geo_mgpxtracksegment', 'start_time', orm['geo.mgpxtracksegment:start_time'])
        
        # Changing field 'MGPXTrackSegment.creation_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime.now))
        db.alter_column('geo_mgpxtracksegment', 'creation_date', orm['geo.mgpxtracksegment:creation_date'])
        
        # Changing field 'MGPXTrackSegment.end_time'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime.now))
        db.alter_column('geo_mgpxtracksegment', 'end_time', orm['geo.mgpxtracksegment:end_time'])
        
        # Changing field 'MGPXTrackSegment.update_date'
        # (to signature: django.db.models.fields.DateTimeField(default=datetime.datetime.now))
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 10, 24, 22, 17, 34, 770012)'}),
            'geometry_collection': ('django.contrib.gis.db.models.fields.GeometryCollectionField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'geo.mgpxtrack': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 10, 24, 22, 17, 34, 770996)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gps_tracks'", 'to': "orm['auth.User']"}),
            'distance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'from_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'to_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 10, 24, 22, 17, 34, 771036)'})
        },
        'geo.mgpxtracksegment': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 10, 24, 22, 17, 34, 771910)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gps_track_segments'", 'to': "orm['auth.User']"}),
            'distance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'from_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'segments'", 'null': 'True', 'to': "orm['geo.MGPXTrack']"}),
            'raw_track': ('SerializedDataField', ["_('raw_track')"], {'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'to_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'track': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 10, 24, 22, 17, 34, 771945)'})
        }
    }
    
    complete_apps = ['geo']
