import requests
from hashlib import md5
import datetime, html, time, random

from django.utils.translation import ugettext as _
from django.shortcuts import render

from django.conf import settings
from apps.orders.models import DeliveryCost
from apps.elephants.models import Categories, Items, Fashions, Sizes, Photo, Balance, RPhoto


def send_sms(phone, text):

    try:
        keys = {}
        keys['version'] = '3.0'
        keys['action'] = 'sendSMS'
        keys['key'] = settings.SMS_PUBLIC_KEY
        keys['sender'] = 'catcult'
        keys['text'] = text
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
    except:
        pass


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


def delivery_cost_sum(country, cart):
    dc_sum = 0
    w = cart.get_weith()
    dc = DeliveryCost.objects.filter(country=country, weigth_from__lte=w, weigth_to__gt=w)
    if dc:
        dc_sum = dc[0].cost
    else:
        dc = DeliveryCost.objects.filter(country=country).order_by('-weigth_to')
        if dc:
            dc_sum = dc[0].cost

    return dc_sum


def delivery_cost(country, cart):

    dc_sum = delivery_cost_sum(country, cart)
    if dc_sum:
        dc = country.name + ' (' + str(dc_sum) + ' ' + _('grn') + ')'
    else:
        dc = country.name

    return dc


def rozetka(request):
    template = 'rozetka.xml'
    cdat = datetime.datetime.now()
    categories = Categories.objects.all().order_by('id')
    # for category in categories:
    #     category.fashions = Fashions.objects.filter(categories=category)
    offers = Items.objects.filter(balance__amount__gt=0, rozetka=True).order_by('id')
    filtered_offers = []
    offers_id = []
    offers_name = []
    for offer in offers:
        offer_name = offer.fashions.categories.name + offer.name + offer.description
        if not offer.id in offers_id and not offer_name in offers_name:
            offers_id.append(offer.id)
            offers_name.append(offer_name)
            for size in Sizes.objects.select_related().filter(balance__item=offer, balance__amount__gt=0):
                offer.sizes = size.name
                # offer.sizes = ', '.join([s.name for s in Sizes.objects.select_related().filter(balance__item=offer, balance__amount__gt=0)])
                offer.pictures = RPhoto.objects.filter(item=offer).order_by('weight')
                balance = Balance.objects.filter(item=offer, size=size)
                stock_quantity = 0
                for item in balance:
                    stock_quantity += item.amount
                offer.stock_quantity = stock_quantity
            filtered_offers.append(offer)
    context = {'offers': filtered_offers, 'categories': categories, 'cdat': cdat}
    return render(request, template, context, content_type='text/xml')
