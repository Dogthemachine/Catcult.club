__author__ = 'flyaway'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Bla-bla.'

    def handle(self, *args, **options):

        from apps.elephants.models import Items

        Items_objects = Items.objects.all()
        for Items_object in Items_objects:
            Items_object.name_ru = Items_object.name
            Items_object.description_ru = Items_object.description
            Items_object.details_ru = Items_object.details
            Items_object.price_description_ru = Items_object.price_description
            Items_object.save()