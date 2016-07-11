__author__ = 'fyaway'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Bla-bla.'

    def handle(self, *args, **options):

        from apps.elephants.models import Item

        Item_objects = Item.objects.all()
        for Item_object in Item_objects:
            Item_object.name_ru = Item_object.name
            Item_object.description_ru = Item_object.description
            Item_object.details_ru = Item_object.details
            Item_object.price_description_ru = Item_object.price_description
            Item_object.save()