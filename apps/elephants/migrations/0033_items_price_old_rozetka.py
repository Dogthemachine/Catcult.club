# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2020-05-30 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0032_auto_20200409_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='price_old_rozetka',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='old price rozetka'),
        ),
    ]
