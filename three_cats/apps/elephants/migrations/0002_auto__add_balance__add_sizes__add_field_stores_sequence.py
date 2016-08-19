# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Balance'
        db.create_table(u'elephants_balance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elephants.Items'])),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elephants.Sizes'])),
            ('amount', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'elephants', ['Balance'])

        # Adding model 'Sizes'
        db.create_table(u'elephants_sizes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('categories', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elephants.Categories'])),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('sequence', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'elephants', ['Sizes'])

        # Removing M2M table for field stores on 'Items'
        db.delete_table(db.shorten_name(u'elephants_items_stores'))

        # Adding field 'Stores.sequence'
        db.add_column(u'elephants_stores', 'sequence',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Balance'
        db.delete_table(u'elephants_balance')

        # Deleting model 'Sizes'
        db.delete_table(u'elephants_sizes')

        # Adding M2M table for field stores on 'Items'
        m2m_table_name = db.shorten_name(u'elephants_items_stores')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('items', models.ForeignKey(orm[u'elephants.items'], null=False)),
            ('stores', models.ForeignKey(orm[u'elephants.stores'], null=False))
        ))
        db.create_unique(m2m_table_name, ['items_id', 'stores_id'])

        # Deleting field 'Stores.sequence'
        db.delete_column(u'elephants_stores', 'sequence')


    models = {
        u'elephants.balance': {
            'Meta': {'object_name': 'Balance'},
            'amount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Items']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Sizes']"})
        },
        u'elephants.categories': {
            'Meta': {'ordering': "('sequence',)", 'object_name': 'Categories'},
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'details_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'details_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'elephants.fashions': {
            'Meta': {'ordering': "('sequence',)", 'object_name': 'Fashions'},
            'categories': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Categories']"}),
            'details': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'details_en': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'details_ru': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'No name'", 'max_length': '70'}),
            'name_en': ('django.db.models.fields.CharField', [], {'default': "'No name'", 'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'default': "'No name'", 'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'elephants.items': {
            'Meta': {'ordering': "('added',)", 'object_name': 'Items'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_ru': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'details_en': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'details_ru': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'fashions': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Fashions']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'price_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'price_description_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'price_description_ru': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'elephants.photo': {
            'Meta': {'ordering': "('added',)", 'object_name': 'Photo'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Items']"})
        },
        u'elephants.sizes': {
            'Meta': {'ordering': "('sequence',)", 'object_name': 'Sizes'},
            'categories': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Categories']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'elephants.stores': {
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

    complete_apps = ['elephants']