import requests
from hashlib import md5

from django.conf import settings
from django.utils.translation import ugettext as _


def send_sms(phone, text, context):
    keys = {}
    keys['version'] = '3.0'
    keys['action'] = 'sendSMS'
    keys['key'] = settings.SMS_PUBLIC_KEY
    keys['sender'] = 'catcult'
    keys['text'] = _(text) % context
    keys['phone'] = phone
    keys['datetime'] = ''
    keys['sms_lifetime'] = '0'

    sum = ''
    for k, v in sorted(keys.items()):
            sum += v
    sum += settings.SMS_PRIVATE_KEY

    checksum = md5(sum.encode('utf-8')).hexdigest()

    url = 'http://api.atompark.com/sms/3.0/sendSMS'

    payload = {
        'sender': keys['sender'],
        'text': text,
        'phone': phone,
        'datetime': keys['datetime'],
        'sms_lifetime': keys['sms_lifetime'],
        'key': settings.SMS_PUBLIC_KEY,
        'sum': checksum
    }

    r = requests.post(url=url, data=payload)


def normalize_phone(phone):
    phone = ''.join(i for i in phone if i.isdigit())

    if len(phone) == 10:
        phone = '38' + phone
    elif len(phone) == 9:
        phone = '380' + phone
    else:
        pass

    if len(phone) == 0:
        phone = 0

    return phone
