from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    args = ''
    help = 'Prepare items for sorting.'

    def handle(self, *args, **options):
        from apps.elephants.models import Items, Sets
        print(timezone.now())
        items = Items.objects.all()

        for item in items:
            views = item.views_month.split(',')

            if len(views) == 30:
                views = views[1:0]
                views.append(str(item.views_today))
                item.views_month = ','.join(views)

            elif len(views) == 0:
                item.views_month += str(item.views_today)

            else:
                item.views_month += ',' + str(item.views_today)

            sum = 0
            for view in item.views_month.split(','):
                try:
                    sum += int(view)
                except:
                    sum += 0

            item.views_today = 0
            item.views = sum
            item.save()


        sets = Sets.objects.all()

        for item in sets:
            views = item.views_month.split(',')

            if len(views) == 30:
                views = views[1:0]
                views.append(str(item.views_today))
                item.views_month = ','.join(views)

            elif len(views) == 0:
                item.views_month += str(item.views_today)

            else:
                item.views_month += ',' + str(item.views_today)

            sum = 0
            for view in item.views_month.split(','):
                try:
                    sum += int(view)
                except:
                    sum += 0

            item.views_today = 0
            item.views = sum
            item.save()
