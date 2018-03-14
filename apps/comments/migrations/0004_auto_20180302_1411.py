# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-02 12:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0003_reply_to_comments_moderated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='city',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='name',
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
