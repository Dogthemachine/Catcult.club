# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-11 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20161011_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='sms_sent',
            field=models.BooleanField(default=False, verbose_name='SMS sent'),
        ),
    ]
