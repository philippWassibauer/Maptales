
from south.db import db
from django.db import models
from geo.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'GeoGeometryTag'
        db.create_table('geo_geogeometrytag', (
            ('id', orm['geo.GeoGeometryTag:id']),
            ('content_type', orm['geo.GeoGeometryTag:content_type']),
            ('object_id', orm['geo.GeoGeometryTag:object_id']),
            ('created_at', orm['geo.GeoGeometryTag:created_at']),
            ('geometry_collection', orm['geo.GeoGeometryTag:geometry_collection']),
        ))
        db.send_create_signal('geo', ['GeoGeometryTag'])
        
        # Adding model 'MGPXTrack'
        db.create_table('geo_mgpxtrack', (
            ('id', orm['geo.MGPXTrack:id']),
            ('title', orm['geo.MGPXTrack:title']),
            ('creation_date', orm['geo.MGPXTrack:creation_date']),
            ('update_date', orm['geo.MGPXTrack:update_date']),
            ('distance', orm['geo.MGPXTrack:distance']),
            ('start_time', orm['geo.MGPXTrack:start_time']),
            ('end_time', orm['geo.MGPXTrack:end_time']),
            ('creator', orm['geo.MGPXTrack:creator']),
            ('from_location_name', orm['geo.MGPXTrack:from_location_name']),
            ('to_location_name', orm['geo.MGPXTrack:to_location_name']),
        ))
        db.send_create_signal('geo', ['MGPXTrack'])
        
        # Adding model 'MGPXTrackSegment'
        db.create_table('geo_mgpxtracksegment', (
            ('id', orm['geo.MGPXTrackSegment:id']),
            ('title', orm['geo.MGPXTrackSegment:title']),
            ('creation_date', orm['geo.MGPXTrackSegment:creation_date']),
            ('update_date', orm['geo.MGPXTrackSegment:update_date']),
            ('distance', orm['geo.MGPXTrackSegment:distance']),
            ('start_time', orm['geo.MGPXTrackSegment:start_time']),
            ('end_time', orm['geo.MGPXTrackSegment:end_time']),
            ('parent', orm['geo.MGPXTrackSegment:parent']),
            ('track', orm['geo.MGPXTrackSegment:track']),
            ('raw_track', orm['geo.MGPXTrackSegment:raw_track']),
            ('creator', orm['geo.MGPXTrackSegment:creator']),
            ('from_location_name', orm['geo.MGPXTrackSegment:from_location_name']),
            ('to_location_name', orm['geo.MGPXTrackSegment:to_location_name']),
        ))
        db.send_create_signal('geo', ['MGPXTrackSegment'])
        
        # Creating unique_together for [content_type, object_id] on GeoGeometryTag.
        db.create_unique('geo_geogeometrytag', ['content_type_id', 'object_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [content_type, object_id] on GeoGeometryTag.
        db.delete_unique('geo_geogeometrytag', ['content_type_id', 'object_id'])
        
        # Deleting model 'GeoGeometryTag'
        db.delete_table('geo_geogeometrytag')
        
        # Deleting model 'MGPXTrack'
        db.delete_table('geo_mgpxtrack')
        
        # Deleting model 'MGPXTrackSegment'
        db.delete_table('geo_mgpxtracksegment')
        
    
    
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'geometry_collection': ('django.contrib.gis.db.models.fields.GeometryCollectionField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'geo.mgpxtrack': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gps_tracks'", 'to': "orm['auth.User']"}),
            'distance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'from_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'to_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'geo.mgpxtracksegment': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gps_track_segments'", 'to': "orm['auth.User']"}),
            'distance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'from_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'segments'", 'null': 'True', 'to': "orm['geo.MGPXTrack']"}),
            'raw_track': ('SerializedDataField', ["_('raw_track')"], {'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'to_location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'track': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }
    
    complete_apps = ['geo']
