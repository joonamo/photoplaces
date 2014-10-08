# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field unprocessed on 'PhotoClusterRun'
        m2m_table_name = db.shorten_name(u'photoplaces_web_photoclusterrun_unprocessed')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photoclusterrun', models.ForeignKey(orm[u'photoplaces_web.photoclusterrun'], null=False)),
            ('photolocationentry', models.ForeignKey(orm[u'photoplaces_web.photolocationentry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['photoclusterrun_id', 'photolocationentry_id'])


    def backwards(self, orm):
        # Removing M2M table for field unprocessed on 'PhotoClusterRun'
        db.delete_table(db.shorten_name(u'photoplaces_web_photoclusterrun_unprocessed'))


    models = {
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
            'end_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
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