# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 19:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advent',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='advent',
            name='user',
        ),
        migrations.RemoveField(
            model_name='advent_tmp',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='advent_tmp',
            name='user',
        ),
        migrations.RemoveField(
            model_name='corrections',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='corrections',
            name='user',
        ),
        migrations.DeleteModel(
            name='Advent',
        ),
        migrations.DeleteModel(
            name='Advent_tmp',
        ),
        migrations.DeleteModel(
            name='Corrections',
        ),
    ]