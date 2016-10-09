# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-08 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', django_resized.forms.ResizedImageField(upload_to='info')),
                ('order', models.SmallIntegerField(default=0, verbose_name='order')),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='added')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Photo Title',
                'verbose_name_plural': 'Photo Titles',
            },
        ),
        migrations.DeleteModel(
            name='Maintitle',
        ),
        migrations.AlterModelOptions(
            name='info',
            options={'verbose_name': 'Info', 'verbose_name_plural': 'Infos'},
        ),
        migrations.AlterModelOptions(
            name='infophoto',
            options={'ordering': ('-added',), 'verbose_name': 'Info Photo', 'verbose_name_plural': 'Info Photos'},
        ),
        migrations.AlterModelOptions(
            name='stores',
            options={'ordering': ('sequence',), 'verbose_name': 'Stores', 'verbose_name_plural': 'Stores'},
        ),
        migrations.RemoveField(
            model_name='info',
            name='address',
        ),
        migrations.RemoveField(
            model_name='info',
            name='latlon',
        ),
        migrations.AlterField(
            model_name='info',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, upload_to='info'),
        ),
        migrations.AlterField(
            model_name='infophoto',
            name='image',
            field=django_resized.forms.ResizedImageField(upload_to='info'),
        ),
        migrations.AlterField(
            model_name='infophoto',
            name='small_image',
            field=django_resized.forms.ResizedImageField(blank=True, upload_to='small_info'),
        ),
        migrations.AlterField(
            model_name='stores',
            name='image',
            field=django_resized.forms.ResizedImageField(upload_to='info'),
        ),
        migrations.AlterField(
            model_name='stores',
            name='small_image',
            field=django_resized.forms.ResizedImageField(blank=True, upload_to='small_info'),
        ),
        migrations.AlterField(
            model_name='stores',
            name='web_address',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='web_address'),
            preserve_default=False,
        ),
    ]