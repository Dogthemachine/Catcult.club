# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Info'
        db.create_table(u'info_info', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('title_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('video', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('info_ru', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('info_en', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('latlon', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'info', ['Info'])

        # Adding model 'Maintitle'
        db.create_table(u'info_maintitle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(default=10)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'info', ['Maintitle'])

        # Adding model 'Infophoto'
        db.create_table(u'info_infophoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['info.Info'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('small_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'info', ['Infophoto'])


    def backwards(self, orm):
        # Deleting model 'Info'
        db.delete_table(u'info_info')

        # Deleting model 'Maintitle'
        db.delete_table(u'info_maintitle')

        # Deleting model 'Infophoto'
        db.delete_table(u'info_infophoto')


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
        }
    }

    complete_apps = ['info']