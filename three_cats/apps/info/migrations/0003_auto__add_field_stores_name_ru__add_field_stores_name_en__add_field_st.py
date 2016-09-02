# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Stores.name_ru'
        db.add_column(u'info_stores', 'name_ru',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Stores.name_en'
        db.add_column(u'info_stores', 'name_en',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Stores.description_ru'
        db.add_column(u'info_stores', 'description_ru',
                      self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True),
                      keep_default=False)

        # Adding field 'Stores.description_en'
        db.add_column(u'info_stores', 'description_en',
                      self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Stores.name_ru'
        db.delete_column(u'info_stores', 'name_ru')

        # Deleting field 'Stores.name_en'
        db.delete_column(u'info_stores', 'name_en')

        # Deleting field 'Stores.description_ru'
        db.delete_column(u'info_stores', 'description_ru')

        # Deleting field 'Stores.description_en'
        db.delete_column(u'info_stores', 'description_en')


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
            'description_en': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_ru': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'order_is_available': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'web_address': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['info']