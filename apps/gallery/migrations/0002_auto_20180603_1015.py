# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-03 07:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='name',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='name_en',
            field=models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='name_ru',
            field=models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='name_uk',
            field=models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='name'),
        ),
    ]
