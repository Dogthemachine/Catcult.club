# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0027_countris'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='delivery_cost',
            field=models.IntegerField(default=0, verbose_name='delivery_cost'),
        ),
    ]
