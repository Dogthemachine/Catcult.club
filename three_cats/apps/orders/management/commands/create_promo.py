from django.core.management.base import BaseCommand, CommandError
from random import choice
from string import ascii_lowercase, ascii_uppercase


class Command(BaseCommand):
    args = ''
    help = 'Creating promo codes.'

    def handle(self, *args, **options):
        from apps.orders.models import Promo

        n = 200;

        while n > 0:

            #code = ''.join(choice(ascii_lowercase+ascii_uppercase+'0123456789') for i in range(5))
            code = ''.join(choice('0123456789') for i in range(5))
            promo = Promo.objects.filter(code=code, used=False)

            if not promo:

                promo = Promo()
                promo.code = code
                promo.discount = 15
                promo.save()

                n -= 1;

                print(code)

