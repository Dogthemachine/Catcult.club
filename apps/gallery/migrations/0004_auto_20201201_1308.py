# Generated by Django 3.1.2 on 2020-12-01 11:08

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_gallery_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=90, size=[2500, 2500], upload_to='photos/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='image_small',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], editable=False, force_format=None, keep_meta=True, quality=90, size=[300, 300], upload_to='small_photos/%Y/%m/%d'),
        ),
    ]
