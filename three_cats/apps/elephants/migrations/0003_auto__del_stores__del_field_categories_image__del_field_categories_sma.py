# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Stores'
        db.delete_table(u'elephants_stores')

        # Deleting field 'Categories.image'
        db.delete_column(u'elephants_categories', 'image')

        # Deleting field 'Categories.small_image'
        db.delete_column(u'elephants_categories', 'small_image')

        # Adding field 'Categories.icon_a'
        db.add_column(u'elephants_categories', 'icon_a',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Categories.icon_b'
        db.add_column(u'elephants_categories', 'icon_b',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Categories.icon_c'
        db.add_column(u'elephants_categories', 'icon_c',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Deleting field 'Fashions.image'
        db.delete_column(u'elephants_fashions', 'image')

        # Deleting field 'Fashions.small_image'
        db.delete_column(u'elephants_fashions', 'small_image')

        # Adding field 'Fashions.icon_a'
        db.add_column(u'elephants_fashions', 'icon_a',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Fashions.icon_b'
        db.add_column(u'elephants_fashions', 'icon_b',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Fashions.icon_c'
        db.add_column(u'elephants_fashions', 'icon_c',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Stores'
        db.create_table(u'elephants_stores', (
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('sequence', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('web_address', self.gf('django.db.models.fields.CharField')(default=None, max_length=250, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description_en', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('order_is_available', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('small_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('description_ru', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal(u'elephants', ['Stores'])

        # Adding field 'Categories.image'
        db.add_column(u'elephants_categories', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Categories.small_image'
        db.add_column(u'elephants_categories', 'small_image',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Deleting field 'Categories.icon_a'
        db.delete_column(u'elephants_categories', 'icon_a')

        # Deleting field 'Categories.icon_b'
        db.delete_column(u'elephants_categories', 'icon_b')

        # Deleting field 'Categories.icon_c'
        db.delete_column(u'elephants_categories', 'icon_c')

        # Adding field 'Fashions.image'
        db.add_column(u'elephants_fashions', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Fashions.small_image'
        db.add_column(u'elephants_fashions', 'small_image',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Deleting field 'Fashions.icon_a'
        db.delete_column(u'elephants_fashions', 'icon_a')

        # Deleting field 'Fashions.icon_b'
        db.delete_column(u'elephants_fashions', 'icon_b')

        # Deleting field 'Fashions.icon_c'
        db.delete_column(u'elephants_fashions', 'icon_c')


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
            'icon_a': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'icon_b': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'icon_c': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'elephants.fashions': {
            'Meta': {'ordering': "('sequence',)", 'object_name': 'Fashions'},
            'categories': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Categories']"}),
            'details': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'details_en': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'details_ru': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'icon_a': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'icon_b': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'icon_c': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'No name'", 'max_length': '70'}),
            'name_en': ('django.db.models.fields.CharField', [], {'default': "'No name'", 'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'default': "'No name'", 'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
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
        }
    }

    complete_apps = ['elephants']