# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0016_stocks_fashions'),
    ]

    operations = [
        migrations.AddField(
            model_name='fashions',
            name='weigth',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='weigth'),
        ),
    ]
