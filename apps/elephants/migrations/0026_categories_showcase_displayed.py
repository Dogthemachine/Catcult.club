# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-09-13 13:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0025_auto_20190825_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='showcase_displayed',
            field=models.BooleanField(default=True, verbose_name='showcase_displayed'),
        ),
    ]