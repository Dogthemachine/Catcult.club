# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-20 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_auto_20170424_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Countris',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Country')),
            ],
            options={
                'verbose_name_plural': 'Countris',
                'ordering': ('name',),
                'verbose_name': 'Countris',
            },
        ),
    ]
