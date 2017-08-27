from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from random import choice
from string import ascii_lowercase, ascii_uppercase


class Command(BaseCommand):
    help = 'Creating promo codes.'

    def add_arguments(self, parser):
        parser.add_argument('n')
        parser.add_argument('discount')

    def handle(self, *args, **options):
        from apps.orders.models import Promo
        print(timezone.now())
        n = int(options['n'])
        discount = int(options['discount'])

        while n > 0:

            #code = ''.join(choice(ascii_lowercase+ascii_uppercase+'0123456789') for i in range(5))
            code = ''.join(choice(ascii_uppercase) for i in range(1)) + ''.join(choice('0123456789') for i in range(4))
            promo = Promo.objects.filter(code=code, used=False)

            if not promo:

                promo = Promo()
                promo.code = code
                promo.discount = discount
                promo.save()

                n -= 1

                print(code)
