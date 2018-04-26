# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-26 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0011_auto_20180312_1510'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='config',
            options={'ordering': ('dollar_rate',), 'verbose_name': 'Config', 'verbose_name_plural': 'Config'},
        ),
        migrations.AlterField(
            model_name='config',
            name='price_description',
            field=models.CharField(default='грн.', max_length=250, verbose_name='price_description'),
        ),
        migrations.AlterField(
            model_name='config',
            name='price_description_en',
            field=models.CharField(default='грн.', max_length=250, null=True, verbose_name='price_description'),
        ),
        migrations.AlterField(
            model_name='config',
            name='price_description_ru',
            field=models.CharField(default='грн.', max_length=250, null=True, verbose_name='price_description'),
        ),
        migrations.AlterField(
            model_name='config',
            name='price_description_uk',
            field=models.CharField(default='грн.', max_length=250, null=True, verbose_name='price_description'),
        ),
    ]
