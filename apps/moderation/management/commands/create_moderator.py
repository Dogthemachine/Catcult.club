from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help = "Create moderator."

    def add_arguments(self, parser):
        parser.add_argument("email", nargs="+", type=str)
        parser.add_argument("first_name", nargs="+", type=str)
        parser.add_argument("last_name", nargs="+", type=str)
        parser.add_argument("password", nargs="+", type=str)

    def handle(self, *args, **options):
        from apps.profiles.models import Moderator

        print(timezone.now())

        user = Moderator()
        user.email = options["email"]
        user.first_name = options["first_name"]
        user.last_name = options["last_name"]
        user.email_checked = True
        user.set_password(options["password"])
        user.save()

        print("User was successfully created")
