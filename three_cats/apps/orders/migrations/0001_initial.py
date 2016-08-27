# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Orders'
        db.create_table(u'orders_orders', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='No name', max_length=70)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('delivery', self.gf('django.db.models.fields.CharField')(default=0, max_length=32)),
            ('payment', self.gf('django.db.models.fields.CharField')(default=0, max_length=32)),
            ('massage', self.gf('django.db.models.fields.TextField')(default='')),
            ('cost', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'orders', ['Orders'])

        # Adding model 'Orderitems'
        db.create_table(u'orders_orderitems', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Orders'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elephants.Items'])),
        ))
        db.send_create_signal(u'orders', ['Orderitems'])

        # Adding model 'Cart'
        db.create_table(u'orders_cart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elephants.Items'])),
            ('session_key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('amount', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'orders', ['Cart'])


    def backwards(self, orm):
        # Deleting model 'Orders'
        db.delete_table(u'orders_orders')

        # Deleting model 'Orderitems'
        db.delete_table(u'orders_orderitems')

        # Deleting model 'Cart'
        db.delete_table(u'orders_cart')


    models = {
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
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'views_per_month': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'orders.cart': {
            'Meta': {'ordering': "('added',)", 'object_name': 'Cart'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'amount': ('django.db.models.fields.SmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Items']"}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'orders.orderitems': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Orderitems'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Items']"}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Orders']"})
        },
        u'orders.orders': {
            'Meta': {'ordering': "('-added',)", 'object_name': 'Orders'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'cost': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'delivery': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '32'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'massage': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'No name'", 'max_length': '70'}),
            'payment': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '32'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['orders']