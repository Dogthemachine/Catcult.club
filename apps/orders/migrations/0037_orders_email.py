# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-11-08 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0036_auto_20190825_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='email'),
        ),
    ]