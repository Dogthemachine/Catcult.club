# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-03 07:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0021_auto_20180215_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='price0',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='cost price'),
        ),
    ]
