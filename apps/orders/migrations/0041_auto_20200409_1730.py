# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2020-04-09 14:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0040_auto_20200331_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iwant',
            name='status',
            field=models.PositiveIntegerField(choices=[(100, 'Новый'), (200, 'Просмотрено'), (230, 'Связались'), (260, 'Не интересно'), (300, 'Изготовлено'), (400, 'Отправлено')], default=100, verbose_name='new status'),
        ),
    ]
