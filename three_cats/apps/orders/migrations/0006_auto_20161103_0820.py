# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-03 06:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20161031_0734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='date_of_delivery',
            field=models.DateField(blank=True, null=True, verbose_name='date_of_delivery'),
        ),
    ]
