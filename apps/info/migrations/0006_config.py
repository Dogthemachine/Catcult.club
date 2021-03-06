# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-12 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0005_auto_20171008_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dollar_rate', models.DecimalField(decimal_places=2, default=1, max_digits=5, verbose_name='dollar rate')),
                ('euro_rate', models.DecimalField(decimal_places=2, default=1, max_digits=5, verbose_name='euro rate')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
