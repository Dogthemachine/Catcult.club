__author__ = 'flyaway'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Bla-bla.'

    def handle(self, *args, **options):

        import datetime
        from apps.elephants.models import Items, Items_views

        items = Items.objects.all()
        date_views = datetime.date.today() - datetime.timedelta(days=30)
        Items_views.objects.exclude(added__gt=date_views).delete()
        for item in items:
            item.views_per_month = Items_views.objects.filter(item=item).count() + 1
            item.save()