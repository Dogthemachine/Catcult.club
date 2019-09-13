# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-08-25 07:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0024_rphoto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rphoto',
            options={'ordering': ('added',), 'verbose_name': 'RozetkaPhoto', 'verbose_name_plural': 'RozetkaPhotos'},
        ),
        migrations.AddField(
            model_name='items',
            name='description_rozetka_a',
            field=models.TextField(blank=True, default='', verbose_name='description rozetka a'),
        ),
        migrations.AddField(
            model_name='items',
            name='description_rozetka_b',
            field=models.TextField(blank=True, default='', verbose_name='description rozetka b'),
        ),
        migrations.AddField(
            model_name='items',
            name='description_rozetka_c',
            field=models.TextField(blank=True, default='', verbose_name='descriptionrozetka c'),
        ),
        migrations.AddField(
            model_name='items',
            name='rozetka',
            field=models.BooleanField(default=False, verbose_name='to rozetka'),
        ),
        migrations.AddField(
            model_name='rphoto',
            name='weight',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='position'),
        ),
    ]