# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PhotoLocationEntry'
        db.create_table(u'photoplaces_web_photolocationentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('username_md5', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('photo_service', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('photo_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('flickr_farm_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('photo_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('photo_thumb_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'photoplaces_web', ['PhotoLocationEntry'])


    def backwards(self, orm):
        # Deleting model 'PhotoLocationEntry'
        db.delete_table(u'photoplaces_web_photolocationentry')


    models = {
        u'photoplaces_web.photolocationentry': {
            'Meta': {'object_name': 'PhotoLocationEntry'},
            'flickr_farm_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'photo_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'photo_service': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'photo_thumb_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'username_md5': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['photoplaces_web']