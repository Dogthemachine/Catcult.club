# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Categories'
        db.create_table(u'elephants_categories', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('small_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('details_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('details_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sequence', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'elephants', ['Categories'])

        # Adding model 'Fashions'
        db.create_table(u'elephants_fashions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='No name', max_length=70)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(default='No name', max_length=70, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(default='No name', max_length=70, null=True, blank=True)),
            ('categories', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elephants.Categories'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('small_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('details_ru', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('details_en', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('sequence', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'elephants', ['Fashions'])

        # Adding model 'Stores'
        db.create_table(u'elephants_stores', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('small_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('description_ru', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('order_is_available', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('web_address', self.gf('django.db.models.fields.CharField')(default=None, max_length=250, null=True, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'elephants', ['Stores'])

        # Adding model 'Items'
        db.create_table(u'elephants_items', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('fashions', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elephants.Fashions'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('small_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('description_ru', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('details_ru', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('details_en', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('price_description', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('price_description_ru', self.gf('django.db.models.fields.CharField')(default='', max_length=250, null=True, blank=True)),
            ('price_description_en', self.gf('django.db.models.fields.CharField')(default='', max_length=250, null=True, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'elephants', ['Items'])

        # Adding M2M table for field stores on 'Items'
        m2m_table_name = db.shorten_name(u'elephants_items_stores')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('items', models.ForeignKey(orm[u'elephants.items'], null=False)),
            ('stores', models.ForeignKey(orm[u'elephants.stores'], null=False))
        ))
        db.create_unique(m2m_table_name, ['items_id', 'stores_id'])

        # Adding model 'Photo'
        db.create_table(u'elephants_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elephants.Items'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'elephants', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'Categories'
        db.delete_table(u'elephants_categories')

        # Deleting model 'Fashions'
        db.delete_table(u'elephants_fashions')

        # Deleting model 'Stores'
        db.delete_table(u'elephants_stores')

        # Deleting model 'Items'
        db.delete_table(u'elephants_items')

        # Removing M2M table for field stores on 'Items'
        db.delete_table(db.shorten_name(u'elephants_items_stores'))

        # Deleting model 'Photo'
        db.delete_table(u'elephants_photo')


    models = {
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
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'stores': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': u"orm['elephants.Stores']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'})
        },
        u'elephants.photo': {
            'Meta': {'ordering': "('added',)", 'object_name': 'Photo'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Items']"})
        },
        u'elephants.stores': {
            'Meta': {'ordering': "('added',)", 'object_name': 'Stores'},
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
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'web_address': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '250', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['elephants']