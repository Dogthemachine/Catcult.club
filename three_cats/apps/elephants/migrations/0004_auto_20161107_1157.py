# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-07 09:57
from __future__ import unicode_literals

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0003_auto_20161026_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='image_en',
            field=django_resized.forms.ResizedImageField(blank=True, upload_to='photos/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='categories',
            name='image_hover_en',
            field=django_resized.forms.ResizedImageField(blank=True, upload_to='photos/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='fashions',
            name='image_en',
            field=django_resized.forms.ResizedImageField(blank=True, upload_to='photos/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='fashions',
            name='image_hover_en',
            field=django_resized.forms.ResizedImageField(blank=True, upload_to='photos/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='sizes',
            name='description_en',
            field=models.TextField(blank=True, default='', null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='sizes',
            name='description_ru',
            field=models.TextField(blank=True, default='', null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='sizes',
            name='name_en',
            field=models.CharField(max_length=20, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='sizes',
            name='name_ru',
            field=models.CharField(max_length=20, null=True, verbose_name='name'),
        ),
    ]