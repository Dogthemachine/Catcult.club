# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-01 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20180228_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply_to_comments',
            name='moderated',
            field=models.BooleanField(default=False, verbose_name='moderated'),
        ),
    ]
