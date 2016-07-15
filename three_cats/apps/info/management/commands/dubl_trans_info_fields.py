__author__ = 'flyaway'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Bla-bla.'

    def handle(self, *args, **options):

        from apps.info.models import Info

        Info_objects = Info.objects.all()
        for Info_object in Info_objects:
            Info_object.title_ru = Info_object.title
            Info_object.info_ru = Info_object.info
            Info_object.save()