# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'PhotoLocationEntry', fields ['location']
        db.create_index(u'photoplaces_web_photolocationentry', ['location'])

        # Adding index on 'PhotoLocationEntry', fields ['username_md5']
        db.create_index(u'photoplaces_web_photolocationentry', ['username_md5'])


    def backwards(self, orm):
        # Removing index on 'PhotoLocationEntry', fields ['username_md5']
        db.delete_index(u'photoplaces_web_photolocationentry', ['username_md5'])

        # Removing index on 'PhotoLocationEntry', fields ['location']
        db.delete_index(u'photoplaces_web_photolocationentry', ['location'])


    models = {
        u'photoplaces_web.photolocationentry': {
            'Meta': {'object_name': 'PhotoLocationEntry'},
            'flickr_farm_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'flickr_server_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'db_index': 'True'}),
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