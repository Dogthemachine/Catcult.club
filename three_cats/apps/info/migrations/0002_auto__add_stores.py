# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stores'
        db.create_table(u'info_stores', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('small_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('order_is_available', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('web_address', self.gf('django.db.models.fields.CharField')(default=None, max_length=250, null=True, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sequence', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'info', ['Stores'])


    def backwards(self, orm):
        # Deleting model 'Stores'
        db.delete_table(u'info_stores')


    models = {
        u'info.info': {
            'Meta': {'object_name': 'Info'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'info_en': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'info_ru': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'latlon': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'topic': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'video': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'})
        },
        u'info.infophoto': {
            'Meta': {'ordering': "('-added',)", 'object_name': 'Infophoto'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'info': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['info.Info']"}),
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'info.maintitle': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Maintitle'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '10'})
        },
        u'info.stores': {
            'Meta': {'ordering': "('sequence',)", 'object_name': 'Stores'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'order_is_available': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'web_address': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['info']