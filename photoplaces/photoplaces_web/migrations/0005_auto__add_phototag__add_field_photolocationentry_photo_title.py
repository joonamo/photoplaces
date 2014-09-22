# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PhotoTag'
        db.create_table(u'photoplaces_web_phototag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'photoplaces_web', ['PhotoTag'])

        # Adding field 'PhotoLocationEntry.photo_title'
        db.add_column(u'photoplaces_web_photolocationentry', 'photo_title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding M2M table for field tags on 'PhotoLocationEntry'
        m2m_table_name = db.shorten_name(u'photoplaces_web_photolocationentry_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photolocationentry', models.ForeignKey(orm[u'photoplaces_web.photolocationentry'], null=False)),
            ('phototag', models.ForeignKey(orm[u'photoplaces_web.phototag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['photolocationentry_id', 'phototag_id'])


    def backwards(self, orm):
        # Deleting model 'PhotoTag'
        db.delete_table(u'photoplaces_web_phototag')

        # Deleting field 'PhotoLocationEntry.photo_title'
        db.delete_column(u'photoplaces_web_photolocationentry', 'photo_title')

        # Removing M2M table for field tags on 'PhotoLocationEntry'
        db.delete_table(db.shorten_name(u'photoplaces_web_photolocationentry_tags'))


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
            'photo_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'photos'", 'symmetrical': 'False', 'to': u"orm['photoplaces_web.PhotoTag']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'username_md5': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'photoplaces_web.phototag': {
            'Meta': {'object_name': 'PhotoTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['photoplaces_web']