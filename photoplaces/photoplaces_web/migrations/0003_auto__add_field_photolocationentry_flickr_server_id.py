# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PhotoLocationEntry.flickr_server_id'
        db.add_column(u'photoplaces_web_photolocationentry', 'flickr_server_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PhotoLocationEntry.flickr_server_id'
        db.delete_column(u'photoplaces_web_photolocationentry', 'flickr_server_id')


    models = {
        u'photoplaces_web.photolocationentry': {
            'Meta': {'object_name': 'PhotoLocationEntry'},
            'flickr_farm_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'flickr_server_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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