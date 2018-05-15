import hashlib
import hmac
import requests

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.dateformat import format


from apps.info.models import Config


class Command(BaseCommand):
    help = 'Updating currency exchange values.'

    def handle(self, *args, **options):
        config = Config.objects.get()

        payload = {}
        payload['transactionType'] = 'CURRENCY_RATES'
        payload['merchantAccount'] = config.merchant_account
        payload['merchantSignature'] = ''
        payload['apiVersion'] = '1'
        payload['orderDate'] = int(format(timezone.now(), 'U'))

        sign_str = ';'.join([
            payload['merchantAccount'], str(payload['orderDate'])
        ])
        payload['merchantSignature'] = hmac.new(
            str.encode(config.merchant_secret),
            str.encode(sign_str),
            hashlib.md5
        ).hexdigest()

        r = requests.post('https://api.wayforpay.com/api', json=payload)

        curr = r.json()['rates']

        config.dollar_rate = curr['USD']
        config.euro_rate = curr['EUR']
        config.save()
