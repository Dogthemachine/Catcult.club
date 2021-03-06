# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-31 09:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0013_auto_20161223_1554'),
        ('orders', '0020_auto_20170131_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='sets',
        ),
        migrations.AddField(
            model_name='cartset',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Cart'),
        ),
        migrations.AddField(
            model_name='cartset',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elephants.Items'),
        ),
    ]
