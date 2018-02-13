# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-13 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0008_auto_20171213_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='description_tag',
            field=models.CharField(blank=True, default='', max_length=160, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='info',
            name='description_tag_en',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='info',
            name='description_tag_ru',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='info',
            name='description_tag_uk',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='info',
            name='title_tag',
            field=models.CharField(blank=True, default='', max_length=70, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='info',
            name='title_tag_en',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='info',
            name='title_tag_ru',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='info',
            name='title_tag_uk',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
    ]
