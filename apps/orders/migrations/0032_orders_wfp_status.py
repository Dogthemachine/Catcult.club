# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-14 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0031_auto_20171212_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='wfp_status',
            field=models.CharField(default='', max_length=64, verbose_name='WFP status'),
        ),
    ]
