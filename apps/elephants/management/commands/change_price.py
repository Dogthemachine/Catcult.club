from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help = "Change price. Multiply to percentage and round to 50"

    def handle(self, *args, **options):
        from apps.elephants.models import Items

        all_items = Items.objects.all()
        for item in all_items:
            item.price = int(item.price * 1.2)
            item.price = 50 * round(item.price / 50)
            item.save()
