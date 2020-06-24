from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime, timedelta


class Command(BaseCommand):
    args = ''
    help = 'Prepare items for sorting on showcase.'

    def handle(self, *args, **options):
        from apps.elephants.models import Items, Sets, Balance
        print(timezone.now())
        items = Items.objects.filter(showcase_displayed=True)

        for item in items:

            showcase_new = False
            showcase_avail = False
            for balance in item.balance_set.all():
                if balance.amount > 0:
                    showcase_avail = True
                    if datetime(item.added.year, item.added.month, item.added.day) < datetime.today() - timedelta(days=15):
                        showcase_new = True

            item.showcase_new = showcase_new
            item.showcase_avail = showcase_avail
            item.save()
