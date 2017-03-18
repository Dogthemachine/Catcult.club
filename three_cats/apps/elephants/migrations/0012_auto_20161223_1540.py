# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-23 13:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0011_auto_20161216_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
                ('image', django_resized.forms.ResizedImageField(upload_to='photos/%Y/%m/%d')),
                ('image_small', django_resized.forms.ResizedImageField(editable=False, upload_to='small_photos/%Y/%m/%d')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('details', models.TextField(blank=True, default='', verbose_name='details')),
                ('price', models.PositiveSmallIntegerField(default=0, verbose_name='price')),
                ('price_description', models.CharField(default='Grn.', max_length=250, verbose_name='price_description')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='views')),
                ('views_today', models.PositiveIntegerField(default=0, verbose_name='views today')),
                ('views_month', models.CharField(default=0, max_length=512, verbose_name='views month')),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='added')),
            ],
            options={
                'ordering': ('-views',),
                'verbose_name_plural': 'Sets',
                'verbose_name': 'Sets',
            },
        ),
        migrations.CreateModel(
            name='SetsPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', django_resized.forms.ResizedImageField(upload_to='photos/%Y/%m/%d')),
                ('image_small', django_resized.forms.ResizedImageField(editable=False, upload_to='small_photos/%Y/%m/%d')),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='added')),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elephants.Sets')),
            ],
            options={
                'ordering': ('added',),
                'verbose_name_plural': 'Sets photos',
                'verbose_name': 'Sets photo',
            },
        ),
        migrations.AddField(
            model_name='categories',
            name='set',
            field=models.BooleanField(default=False, verbose_name='set'),
        ),
        migrations.AddField(
            model_name='sets',
            name='categories',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elephants.Categories'),
        ),
        migrations.AddField(
            model_name='sets',
            name='items',
            field=models.ManyToManyField(to='elephants.Items'),
        ),
    ]