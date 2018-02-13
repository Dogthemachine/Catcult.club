# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-13 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0019_items_showcase_displayed'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='description_tag',
            field=models.CharField(blank=True, default='', max_length=160, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='categories',
            name='description_tag_en',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='categories',
            name='description_tag_ru',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='categories',
            name='description_tag_uk',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='categories',
            name='title_tag',
            field=models.CharField(blank=True, default='', max_length=70, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='categories',
            name='title_tag_en',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='categories',
            name='title_tag_ru',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='categories',
            name='title_tag_uk',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='fashions',
            name='description_tag',
            field=models.CharField(blank=True, default='', max_length=160, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='fashions',
            name='description_tag_en',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='fashions',
            name='description_tag_ru',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='fashions',
            name='description_tag_uk',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='fashions',
            name='title_tag',
            field=models.CharField(blank=True, default='', max_length=70, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='fashions',
            name='title_tag_en',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='fashions',
            name='title_tag_ru',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='fashions',
            name='title_tag_uk',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='items',
            name='description_tag',
            field=models.CharField(blank=True, default='', max_length=160, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='items',
            name='description_tag_en',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='items',
            name='description_tag_ru',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='items',
            name='description_tag_uk',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='items',
            name='title_tag',
            field=models.CharField(blank=True, default='', max_length=70, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='items',
            name='title_tag_en',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='items',
            name='title_tag_ru',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='items',
            name='title_tag_uk',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='sets',
            name='description_tag',
            field=models.CharField(blank=True, default='', max_length=160, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='sets',
            name='description_tag_en',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='sets',
            name='description_tag_ru',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='sets',
            name='description_tag_uk',
            field=models.CharField(blank=True, default='', max_length=160, null=True, verbose_name='description tag'),
        ),
        migrations.AddField(
            model_name='sets',
            name='title_tag',
            field=models.CharField(blank=True, default='', max_length=70, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='sets',
            name='title_tag_en',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='sets',
            name='title_tag_ru',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
        migrations.AddField(
            model_name='sets',
            name='title_tag_uk',
            field=models.CharField(blank=True, default='', max_length=70, null=True, verbose_name='title tag'),
        ),
    ]