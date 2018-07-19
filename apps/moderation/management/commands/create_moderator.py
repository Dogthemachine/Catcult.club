from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    args = '<email> <first_name> <last_name> <password>'
    help = 'Merge today views with all views for plot.'

    def handle(self, *args, **options):
        from apps.profiles.models import Moderator

        print(timezone.now())

        user = Moderator()
        user.email = args[0]
        user.first_name = args[1]
        user.last_name = args[2]
        user.email_checked = True
        user.set_password(args[3])
        user.save()

        print('User was successfully created')