# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-03 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20161103_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='user_comment',
            field=models.CharField(blank=True, max_length=512, verbose_name='user comment'),
        ),
    ]
