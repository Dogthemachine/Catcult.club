# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Orders.number'
        db.add_column(u'orders_orders', 'number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)

        # Deleting field 'Orderitems.item'
        db.delete_column(u'orders_orderitems', 'item_id')

        # Adding field 'Orderitems.balance'
        db.add_column(u'orders_orderitems', 'balance',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['elephants.Balance']),
                      keep_default=False)

        # Deleting field 'Cart.item'
        db.delete_column(u'orders_cart', 'item_id')

        # Adding field 'Cart.balance'
        db.add_column(u'orders_cart', 'balance',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['elephants.Balance']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Orders.number'
        db.delete_column(u'orders_orders', 'number')

        # Adding field 'Orderitems.item'
        db.add_column(u'orders_orderitems', 'item',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['elephants.Items']),
                      keep_default=False)

        # Deleting field 'Orderitems.balance'
        db.delete_column(u'orders_orderitems', 'balance_id')

        # Adding field 'Cart.item'
        db.add_column(u'orders_cart', 'item',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['elephants.Items']),
                      keep_default=False)

        # Deleting field 'Cart.balance'
        db.delete_column(u'orders_cart', 'balance_id')


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
            'price_description': ('django.db.models.fields.CharField', [], {'default': "u'Grn.'", 'max_length': '250'}),
            'price_description_en': ('django.db.models.fields.CharField', [], {'default': "u'Grn.'", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'price_description_ru': ('django.db.models.fields.CharField', [], {'default': "u'Grn.'", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'views_per_month': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'elephants.sizes': {
            'Meta': {'ordering': "('sequence',)", 'object_name': 'Sizes'},
            'categories': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Categories']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sequence': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'orders.cart': {
            'Meta': {'ordering': "('added',)", 'object_name': 'Cart'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'amount': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'balance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Balance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'orders.orderitems': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Orderitems'},
            'balance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elephants.Balance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Orders']"})
        },
        u'orders.orders': {
            'Meta': {'ordering': "('-added',)", 'object_name': 'Orders'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'cost': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'delivery': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '32'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'massage': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'No name'", 'max_length': '70'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'payment': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '32'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['orders']