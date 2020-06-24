# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2020-02-14 07:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0038_iwant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iwant',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'Новый'), (2, 'Просмотрено'), (3, 'Изготовлено'), (4, 'Отправлено')], default=1, verbose_name='new status'),
        ),
    ]