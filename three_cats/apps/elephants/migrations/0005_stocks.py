# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-24 09:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0004_auto_20161107_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stocks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
                ('name_ru', models.CharField(max_length=250, null=True, verbose_name='name')),
                ('name_en', models.CharField(max_length=250, null=True, verbose_name='name')),
                ('image', django_resized.forms.ResizedImageField(upload_to='photos/%Y/%m/%d')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('description_ru', models.TextField(blank=True, default='', null=True, verbose_name='description')),
                ('description_en', models.TextField(blank=True, default='', null=True, verbose_name='description')),
                ('discount', models.PositiveSmallIntegerField(default=0, verbose_name='diccount')),
                ('action_begin', models.DateField(verbose_name='action_begin')),
                ('action_end', models.DateField(verbose_name='action_end')),
                ('categories', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='elephants.Categories')),
            ],
            options={
                'verbose_name': 'stocks',
                'verbose_name_plural': 'stocks',
                'ordering': ('action_begin',),
            },
        ),
    ]