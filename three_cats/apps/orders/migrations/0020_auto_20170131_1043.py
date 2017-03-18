# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-31 08:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0013_auto_20161223_1554'),
        ('orders', '0019_auto_20170126_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='sets',
        ),
        migrations.AddField(
            model_name='cart',
            name='sets',
            field=models.ManyToManyField(blank=True, to='elephants.Sets'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='amount_set',
            field=models.PositiveIntegerField(default=0),
        ),
    ]