# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-11 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0014_auto_20170216_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='details_uk',
            field=models.TextField(blank=True, null=True, verbose_name='details'),
        ),
        migrations.AddField(
            model_name='categories',
            name='name_uk',
            field=models.CharField(max_length=70, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='fashions',
            name='details_uk',
            field=models.TextField(blank=True, default='', null=True, verbose_name='details'),
        ),
        migrations.AddField(
            model_name='fashions',
            name='name_uk',
            field=models.CharField(default='No name', max_length=70, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='items',
            name='description_uk',
            field=models.TextField(blank=True, default='', null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='items',
            name='details_uk',
            field=models.TextField(blank=True, default='', null=True, verbose_name='details'),
        ),
        migrations.AddField(
            model_name='items',
            name='name_uk',
            field=models.CharField(max_length=250, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='items',
            name='price_description_uk',
            field=models.CharField(default='Grn.', max_length=250, null=True, verbose_name='price_description'),
        ),
        migrations.AddField(
            model_name='sets',
            name='description_uk',
            field=models.TextField(blank=True, default='', null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='sets',
            name='details_uk',
            field=models.TextField(blank=True, default='', null=True, verbose_name='details'),
        ),
        migrations.AddField(
            model_name='sets',
            name='name_uk',
            field=models.CharField(max_length=250, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='sets',
            name='price_description_uk',
            field=models.CharField(default='Grn.', max_length=250, null=True, verbose_name='price_description'),
        ),
        migrations.AddField(
            model_name='sizes',
            name='description_uk',
            field=models.TextField(blank=True, default='', null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='sizes',
            name='name_uk',
            field=models.CharField(max_length=20, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='stocks',
            name='description_uk',
            field=models.TextField(blank=True, default='', null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='stocks',
            name='name_uk',
            field=models.CharField(max_length=250, null=True, verbose_name='name'),
        ),
    ]
