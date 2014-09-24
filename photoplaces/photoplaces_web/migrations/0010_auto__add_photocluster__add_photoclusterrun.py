# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PhotoCluster'
        db.create_table(u'photoplaces_web_photocluster', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('run', self.gf('django.db.models.fields.related.ForeignKey')(related_name='clusters', to=orm['photoplaces_web.PhotoClusterRun'])),
            ('center', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('bounding_shape', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
        ))
        db.send_create_signal(u'photoplaces_web', ['PhotoCluster'])

        # Adding M2M table for field photos on 'PhotoCluster'
        m2m_table_name = db.shorten_name(u'photoplaces_web_photocluster_photos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photocluster', models.ForeignKey(orm[u'photoplaces_web.photocluster'], null=False)),
            ('photolocationentry', models.ForeignKey(orm[u'photoplaces_web.photolocationentry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['photocluster_id', 'photolocationentry_id'])

        # Adding model 'PhotoClusterRun'
        db.create_table(u'photoplaces_web_photoclusterrun', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('algorithm', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, db_index=True)),
            ('messages', self.gf('django.db.models.fields.TextField')()),
            ('density_eps', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('density_min_pts', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'photoplaces_web', ['PhotoClusterRun'])


    def backwards(self, orm):
        # Deleting model 'PhotoCluster'
        db.delete_table(u'photoplaces_web_photocluster')

        # Removing M2M table for field photos on 'PhotoCluster'
        db.delete_table(db.shorten_name(u'photoplaces_web_photocluster_photos'))

        # Deleting model 'PhotoClusterRun'
        db.delete_table(u'photoplaces_web_photoclusterrun')


    models = {
        u'photoplaces_web.photocluster': {
            'Meta': {'object_name': 'PhotoCluster'},
            'bounding_shape': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {}),
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
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'})
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