# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-12 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0010_auto_20180215_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='media',
            field=models.CharField(default='https://catcult.club/media/', max_length=250, verbose_name='media url'),
        ),
        migrations.AddField(
            model_name='config',
            name='static',
            field=models.CharField(default='https://catcult.club/static/', max_length=250, verbose_name='static url'),
        ),
    ]
