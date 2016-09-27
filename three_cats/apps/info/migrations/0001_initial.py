# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-09 21:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='topic')),
                ('title', models.CharField(blank=True, max_length=250, verbose_name='name')),
                ('title_ru', models.CharField(blank=True, max_length=250, null=True, verbose_name='name')),
                ('title_en', models.CharField(blank=True, max_length=250, null=True, verbose_name='name')),
                ('image', models.ImageField(blank=True, upload_to='info')),
                ('video', models.CharField(blank=True, default='', max_length=1000, verbose_name='video')),
                ('info', models.TextField(blank=True, default='', verbose_name='text')),
                ('info_ru', models.TextField(blank=True, default='', null=True, verbose_name='text')),
                ('info_en', models.TextField(blank=True, default='', null=True, verbose_name='text')),
                ('address', models.CharField(blank=True, max_length=250, verbose_name='address')),
                ('latlon', models.CharField(blank=True, max_length=50, verbose_name='lat lon')),
            ],
            options={
                'verbose_name_plural': 'Info',
                'verbose_name': 'Info',
            },
        ),
        migrations.CreateModel(
            name='Infophoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='info')),
                ('small_image', models.ImageField(blank=True, editable=False, upload_to='small_info')),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='added')),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Info')),
            ],
            options={
                'verbose_name_plural': 'Info Photo',
                'verbose_name': 'Info Photo',
                'ordering': ('-added',),
            },
        ),
        migrations.CreateModel(
            name='Maintitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='info')),
                ('order', models.SmallIntegerField(default=10, verbose_name='order')),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='added')),
            ],
            options={
                'verbose_name_plural': 'Photo Title',
                'verbose_name': 'Photo Title',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Stores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
                ('name_ru', models.CharField(max_length=250, null=True, verbose_name='name')),
                ('name_en', models.CharField(max_length=250, null=True, verbose_name='name')),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d')),
                ('small_image', models.ImageField(blank=True, editable=False, upload_to='small_photos/%Y/%m/%d')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('description_ru', models.TextField(blank=True, default='', null=True, verbose_name='description')),
                ('description_en', models.TextField(blank=True, default='', null=True, verbose_name='description')),
                ('order_is_available', models.PositiveSmallIntegerField(default=0, verbose_name='order is available')),
                ('web_address', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='web_address')),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='added')),
                ('sequence', models.PositiveSmallIntegerField(default=0, verbose_name='sequence')),
            ],
            options={
                'verbose_name_plural': 'stores',
                'verbose_name': 'stores',
                'ordering': ('sequence',),
            },
        ),
    ]
