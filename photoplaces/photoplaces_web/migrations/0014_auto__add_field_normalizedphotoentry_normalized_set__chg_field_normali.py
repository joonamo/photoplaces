# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'NormalizedPhotoEntry.normalized_set'
        db.add_column(u'photoplaces_web_normalizedphotoentry', 'normalized_set',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='entries', to=orm['photoplaces_web.NormalizedPhotoSet']),
                      keep_default=False)


        # Changing field 'NormalizedPhotoEntry.actual_photo'
        db.alter_column(u'photoplaces_web_normalizedphotoentry', 'actual_photo_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photoplaces_web.PhotoLocationEntry']))

    def backwards(self, orm):
        # Deleting field 'NormalizedPhotoEntry.normalized_set'
        db.delete_column(u'photoplaces_web_normalizedphotoentry', 'normalized_set_id')


        # Changing field 'NormalizedPhotoEntry.actual_photo'
        db.alter_column(u'photoplaces_web_normalizedphotoentry', 'actual_photo_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photoplaces_web.NormalizedPhotoSet']))

    models = {
        u'photoplaces_web.normalizedphotoentry': {
            'Meta': {'object_name': 'NormalizedPhotoEntry'},
            'actual_photo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['photoplaces_web.PhotoLocationEntry']"}),
            'hour': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'month': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'normalized_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['photoplaces_web.NormalizedPhotoSet']"})
        },
        u'photoplaces_web.normalizedphotoset': {
            'Meta': {'object_name': 'NormalizedPhotoSet'},
            'hour_deviation': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hour_mean': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_x_deviation': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_x_mean': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_y_deviation': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_y_mean': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'month_deviation': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'month_mean': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'photoplaces_web.photocluster': {
            'Meta': {'object_name': 'PhotoCluster'},
            'bounding_shape': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'bounding_shape_dirty': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'center_dirty': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'clusters'", 'symmetrical': 'False', 'to': u"orm['photoplaces_web.PhotoLocationEntry']"}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clusters'", 'to': u"orm['photoplaces_web.PhotoClusterRun']"})
        },
        u'photoplaces_web.photoclusterrun': {
            'Meta': {'object_name': 'PhotoClusterRun'},
            'algorithm': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'density_eps': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'density_min_pts': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.TextField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'W'", 'max_length': '1', 'db_index': 'True'}),
            'unprocessed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': u"orm['photoplaces_web.PhotoLocationEntry']"})
        },
        u'photoplaces_web.photolocationentry': {
            'Meta': {'object_name': 'PhotoLocationEntry'},
            'flickr_farm_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'flickr_server_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'photo_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'photo_service': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'photo_thumb_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'photos'", 'symmetrical': 'False', 'to': u"orm['photoplaces_web.PhotoTag']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'username_md5': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        },
        u'photoplaces_web.phototag': {
            'Meta': {'object_name': 'PhotoTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['photoplaces_web']