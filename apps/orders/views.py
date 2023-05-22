# -*- coding: utf-8 -*-
import base64
import json
import hashlib
import hmac
from jsonview.decorators import json_view

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.template import loader, Context
from django.utils.translation import gettext as _
from django.db.models import Sum
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from django.utils.dateformat import format

from .forms import CheckoutForm
from .models import Cart, CartItem, CartSet, CartSetItem, Orders, OrderItems, Payment, PaymentRaw, Promo, Phones, \
    NovaPoshtaCities, NovaPoshtaWarehouses, NovaPoshtaRegions
from apps.info.models import Config
from apps.liqpay import LiqPay
from apps.elephants.models import Balance
from apps.helpers import normalize_phone, send_sms, delivery_cost_sum


@json_view
def cart(request):
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    cart.session = request.session.session_key
    cart.save()

    if not created:
        cart_items = CartItem.objects.filter(cart=cart)
        for c_i in cart_items:
            c_i.bal = Balance.objects.get(item=c_i.item, size=c_i.size).amount
    else:
        cart_items = []

    t = loader.get_template('orders/cart.html')
    c = {'cart': cart, 'cart_items': cart_items}
    html = t.render(c, request)

    return {'html': html}


@json_view
def cart_remove(request, id, set=False):
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)

    if not created:
        if set:
            try:
                cart_set = CartSet.objects.get(id=id)
            except:
                raise
                return {'success': False}
            else:
                set_items = CartSetItem.objects.filter(cartset=cart_set)
                for item in set_items:
                    try:
                        cart_item = CartItem.objects.get(item=item.item, size=item.size)
                    except CartItem.DoesNotExist:
                        raise
                        return {'success': False}
                    else:
                        cart_item.amount -= cart_set.amount
                        cart_item.amount_set -= cart_set.amount
                        cart_item.save()

                        if cart_item.amount == 0:
                            cart_item.delete()

                cart_set.delete()

        else:
            try:
                cart_item = CartItem.objects.get(id=id)
            except CartItem.DoesNotExist:
                return {'success': False}
            else:
                cart_item.amount = cart_item.amount_set
                cart_item.save()

                if cart_item.amount == 0:
                    cart_item.delete()
    else:
        return {'success': False}

    cart_items = CartItem.objects.filter(cart=cart)
    for c_i in cart_items:
        c_i.bal = Balance.objects.get(item=c_i.item, size=c_i.size).amount
    t = loader.get_template('orders/cart.html')
    c = {'cart': cart, 'cart_items': cart_items}
    html = t.render(c, request)

    return {'html': html, 'count': cart_items.count()}


@json_view
def cart_plus(request, id, set=False, plus=True):
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    if not created:
        if not set:
            try:
                cart_item = CartItem.objects.get(id=id)
            except CartItem.DoesNotExist:
                return {'success': False}
            else:
                if plus:
                    cart_item.amount += 1
                else:
                    cart_item.amount -= 1
                cart_item.save()
    else:
        return {'success': False}

    cart_items = CartItem.objects.filter(cart=cart)
    for c_i in cart_items:
        c_i.bal = Balance.objects.get(item=c_i.item, size=c_i.size).amount
    t = loader.get_template('orders/cart.html')
    c = {'cart': cart, 'cart_items': cart_items}
    html = t.render(c, request)

    return {'html': html, 'count': cart_items.count()}


@json_view
def cart_warehouses(request, city_id, warehouse_id):
    warehouses = [(w.id, w.description, w.id == warehouse_id) for w in
                  NovaPoshtaWarehouses.objects.filter(novaposhtacities__id=city_id).order_by('number')]
    return {'success': True, 'warehouses': warehouses}


@json_view
def cart_cities(request, region_id, city_id):
    try:
        region = NovaPoshtaRegions.objects.get(pk=region_id)
    except:
        return {'success': False}
    if city_id == 0:
        cities = [(c.id, c.description, region.areasenter_ref == c.ref) for c in
                  NovaPoshtaCities.objects.filter(novaposhtaregions__id=region_id)]
    else:
        cities = [(c.id, c.description, city_id == c.id) for c in
                  NovaPoshtaCities.objects.filter(novaposhtaregions__id=region_id)]
    return {'success': True, 'cities': cities}


def price_description(request):
    config = Config.objects.get()
    description = ''
    if request.session['valuta']=='grn':
        description = config.price_description
    if request.session['valuta']=='usd':
        description = config.price_description_usd
    if request.session['valuta']=='eur':
        description = config.price_description_eur

    return description


@json_view
def cart_checkout(request):
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)

    if created:
        return {'success': False}

    form = CheckoutForm(request.user, cart=cart, language=request.LANGUAGE_CODE)

    no_avail_items = 0

    cart_items = CartItem.objects.filter(cart=cart)

    print('\n\n\n', request.LANGUAGE_CODE, '\n\n\n')
    print('\n\n\n', request.META['HTTP_ACCEPT_LANGUAGE'], '\n\n\n')

    for item in cart_items:
        if not item.check_avail():
            no_avail_items += 1

    if no_avail_items:

        t = loader.get_template('orders/cart.html')
        c = {'cart': cart, 'cart_items': cart_items}
        html = t.render(c, request)

        return {'form': False, 'html': html}

    if request.method == 'POST':
        form = CheckoutForm(request.user, request.POST, cart=cart, language=request.LANGUAGE_CODE)
        if form.is_valid():

            discount_stocks = int(cart.get_discount())

            discount_promo = 0
            if not discount_stocks:
                if form.cleaned_data['promo']:
                    if discount_stocks == 0:
                        codes = Promo.objects.filter(code=form.cleaned_data['promo'], used=False)
                        if codes:
                            code = codes[0]
                            discount_promo = code.discount
                            code.used = True
                            code.save()

                            message1 = _('Thank you. Your bonus %s percent activated.') % code.discount
                            messages.add_message(
                                request,
                                messages.SUCCESS,
                                message1
                            )
                    else:
                        message1 = _('Your discount on the share is %(sum)s %(dsc)s.<br/>') % {'sum': cart.discount_stocks_val(request), 'dsc': price_description(request)}
                        message1 += _('Your promo-code is not activated.')
                        messages.add_message(
                            request,
                            messages.SUCCESS,
                            message1
                        )

            phone = Phones.objects.filter(phone=normalize_phone(form.cleaned_data['phone']))

            if phone:
                p = phone[0]
                if discount_stocks == 0 and discount_promo == 0 and p.active:
                    discount_promo = settings.DISCOUNT_PHONE

                    message0 = _('Thank you. Your discount is %s percent.<br/>') % settings.DISCOUNT_PHONE
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        message0
                    )
                p.news = True
                p.save()

            else:
                p = Phones()
                p.phone = normalize_phone(form.cleaned_data['phone'])
                p.lang_code = request.LANGUAGE_CODE
                p.save()

                message0 = _('Thank you. After payment of the order your discount will be %s percent.<br/>') % settings.DISCOUNT_PHONE
                message0 += '<a href="%(url)s">%(text)s</a>' % ({'url': reverse('messages_off', args=(p.id,)), 'text': _('Do not recive messages about promotion.')})
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    message0
                )

            delivery_cost = 0
            if form.cleaned_data['delivery'] == 3:
                delivery_cost = delivery_cost_sum(form.cleaned_data['country'], cart)

            order = Orders()
            order.name = form.cleaned_data['name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = normalize_phone(form.cleaned_data['phone'])
            order.email = form.cleaned_data['email']
            order.lang_code = request.LANGUAGE_CODE
            order.payment_method = form.cleaned_data['payment']
            order.delivery_method = form.cleaned_data['delivery']
            order.user_comment = form.cleaned_data['shipping']
            order.delivery_cost = delivery_cost
            order.discount_promo = discount_promo
            order.discount_stocks = cart.discount_stocks
            if form.cleaned_data['payment']==5:
                order.paid = True
                order.ttn = 0
                order.date_of_delivery = timezone.now()
                order.delivered = True
                order.packed = True
            order.save()

            cart_items = CartItem.objects.filter(cart=cart)

            for item in cart_items:
                balance = Balance.objects.get(item=item.item, size=item.size)

                orderitem = OrderItems()
                orderitem.order = order
                orderitem.balance = balance
                orderitem.amount = item.amount
                orderitem.price = item.item.get_actual_price()
                orderitem.save()

            items = OrderItems.objects.filter(order=order)
            sum = 0

            for i in items:
                sum += i.price * i.amount

            order.discount_set = sum - cart.get_total()
            order.save()

            if form.cleaned_data['payment'] == 5:
                p = Payment()
                p.order = order
                p.amount = order.get_total_price_grn()
                p.comment = _('In showroom')
                p.save()

            cart.delete()

            if order.payment_method == 2:
                if order.lang_code == 'en':
                    text = 'Your order #%(number)s has been taken. Card number is %(card)s (%(name)s) and sum is %(sum)s %(dsc)s. CatCult' % {'number': order.get_number(), 'card': settings.PRIVAT_CARD, 'name': settings.PRIVAT_NAME, 'sum': order.get_total_price(request), 'dsc': price_description(request)}
                    text += ' Please indicate your name or order number in the payment order'
                elif order.lang_code == 'ru':
                    text = 'Ваш заказ №%(number)s был принят. Номер карты %(card)s (%(name)s). Сумма к оплате %(sum)s %(dsc)s. CatCult' % {'number': order.get_number(), 'card': settings.PRIVAT_CARD, 'name': settings.PRIVAT_NAME, 'sum': order.get_total_price(request), 'dsc': price_description(request)}
                    text += ' Пожалуйста, укажите в назначении платежа свою фамилию или номер заказа'
                elif order.lang_code == 'uk':
                    text = 'Ваше замовлення №%(number)s було прийняте. Номер картки %(card)s (%(name)s). Сума до оплати %(sum)s %(dsc)s. CatCult' % {'number': order.get_number(), 'card': settings.PRIVAT_CARD, 'name': settings.PRIVAT_NAME, 'sum': order.get_total_price(request), 'dsc': price_description(request)}
                    text += ' Буьласка, вкжіть в призначенні платежу своє прізвище або номер замовлення'
                else:
                    text = ''

                send_sms(order.phone, text)

            elif order.payment_method == 1:
                if order.lang_code == 'en':
                    text = 'Your order #%(number)s has been taken. Card number is %(card)s (%(name)s) and sum is %(sum)s %(dsc)s. CatCult' % {'number': order.get_number(), 'card': settings.MONO_CARD, 'name': settings.MONO_NAME, 'sum': order.get_total_price(request), 'dsc': price_description(request)}
                    text += ' Please indicate your name or order number in the payment order'
                elif order.lang_code == 'ru':
                    text = 'Ваш заказ №%(number)s был принят. Номер карты %(card)s (%(name)s). Сумма к оплате %(sum)s %(dsc)s. CatCult' % {'number': order.get_number(), 'card': settings.MONO_CARD, 'name': settings.MONO_NAME, 'sum': order.get_total_price(request), 'dsc': price_description(request)}
                    text += ' Пожалуйста, укажите в назначении платежа свою фамилию или номер заказа'
                elif order.lang_code == 'uk':
                    text = 'Ваше замовлення №%(number)s було прийняте. Номер картки %(card)s (%(name)s). Сума до оплати %(sum)s %(dsc)s. CatCult' % {'number': order.get_number(), 'card': settings.MONO_CARD, 'name': settings.MONO_NAME, 'sum': order.get_total_price(request), 'dsc': price_description(request)}
                    text += ' Буьласка, вкжіть в призначенні платежу своє прізвище або номер замовлення'
                else:
                    text = ''

                send_sms(order.phone, text)

            else:
                if order.payment_method != 5:
                    if order.lang_code == 'en':
                        text = 'Your order #%(number)s has been taken. Total price is %(sum)s %(dsc)s. CatCult' % {'number': order.get_number(), 'sum': order.get_total_price(request), 'dsc': price_description(request)}
                        text += ' Please indicate your name or order number in the payment order'
                    elif order.lang_code == 'ru':
                        text = 'Ваш заказ №%(number)s был принят. Сумма к оплате %(sum)s %(dsc)s. CatCult' % {'number': order.get_number(), 'sum': order.get_total_price(request), 'dsc': price_description(request)}
                        text += ' Пожалуйста, укажите в назначении платежа свою фамилию или номер заказа'
                    elif order.lang_code == 'uk':
                        text = 'Ваше замовлення №%(number)s було прийняте. Сума до оплати %(sum)s %(dsc)s. CatCult' % {'number': order.get_number(), 'sum': order.get_total_price(request), 'dsc': price_description(request)}
                        text += ' Буьласка, вкжіть в призначенні платежу своє прізвище або номер замовлення'
                    else:
                        text = ''

                    if order.payment_method == 0:
                        send_sms(order.phone, text)

            if order.payment_method != 5:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    text
                )

            if order.phone:
                try:
                    ph_s = str(order.phone)
                except:
                    ph_s = _('Error in phone number.')
            else:
                ph_s = _('Phone number is not set.')

            message = _('Your order has been placed. We will contact you shortly.<br/>Order details:<br/>')
            message += str(order.get_number()) + '<br/>' + ph_s + '<br/>'
            for item in order.orderitems_set.all():
                message += item.balance.item.name + ' - '
                message += item.balance.size.name + ' - '
                message += str(item.amount) + '<br/>'
            if delivery_cost:
                if request.session['valuta'] == 'grn':
                    pass
                else:
                    config = Config.objects.get()
                    rate = 1
                    if request.session['valuta'] == 'usd':
                        rate = config.dollar_rate
                    if request.session['valuta'] == 'eur':
                        rate = config.euro_rate
                    delivery_cost = round(delivery_cost / rate, 2)
                message += _('Cost of delivery:') + ' ' + str(delivery_cost) + ' ' + price_description(request) + '<br/>'
            message += _('Total:') + ' ' + str(order.get_total_price(request)) + ' ' + price_description(request) + '<br/>'

            messages.add_message(
                request,
                messages.SUCCESS,
                message
            )

            if order.payment_method == 3:
                """
                LiqPay form below.
                """
                """
                liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
                payment_form = liqpay.cnb_form({
                    'action': 'pay',
                    'amount': order.get_total_price_grn(),
                    'currency': 'UAH',
                    'description': 'CatCult order',
                    'order_id': order.id,
                    'server_url': settings.LIQPAY_CALLBACK,
                    'result_url': settings.LIQPAY_SUCCESS
                })

                return {'payment_form': payment_form}
                """
                config = Config.objects.get()
                payment = {}
                payment['account'] = config.merchant_account
                payment['domain'] = config.merchant_domain_name
                payment['tr_type'] = 'SALE'
                payment['auth_type'] = 'SimpleSignature'
                payment['sign'] = ''
                payment['url'] = 'https://' + config.merchant_domain_name + reverse('wfp_callback')
                payment['order_id'] = order.id
                payment['order_date'] = format(order.added, 'U')
                payment['amount'] = order.get_total_price_grn()
                payment['currency'] = 'UAH'
                payment['products'] = []
                payment['prices'] = []
                payment['counts'] = []
                payment['first_name'] = order.name
                payment['last_name'] = order.last_name
                payment['phone'] = order.phone
                payment['lang'] = 'AUTO'

                for order_item in order.orderitems_set.all():
                    payment['products'].append(order_item.balance.item.name)
                    payment['prices'].append(order_item.price)
                    payment['counts'].append(order_item.amount)

                products_str = ';'.join(payment['products'])
                prices_str = ';'.join(str(x) for x in payment['prices'])
                counts_str = ';'.join(str(x) for x in payment['counts'])

                sign_str = ';'.join([
                    payment['account'], payment['domain'], str(payment['order_id']),
                    str(payment['order_date']), str(payment['amount']), payment['currency'],
                    products_str, str(counts_str), str(prices_str)
                ])
                payment['sign'] = hmac.new(
                    str.encode(config.merchant_secret),
                    str.encode(sign_str),
                    hashlib.md5
                ).hexdigest()

                return {'payment': payment}

            return {'form': False}

    t = loader.get_template('orders/cart_checkout.html')
    c = {'form': form}
    html = t.render(c, request)

    button_text = _('Place the order')

    return {'form': True, 'html': html, 'button_text': button_text}


@csrf_exempt
def liqpay_callback(request):
    if request.method == 'POST':
        raw = PaymentRaw()
        raw.data = request.POST.get('data', '')
        raw.sign = request.POST.get('signature', '')
        try:
            raw.data_decoded = base64.b64decode(request.POST.get('data', '')).decode()
        except:
            pass
        raw.save()

        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        sign = liqpay.str_to_sign(
            settings.LIQPAY_PRIVATE_KEY +
            request.POST.get('data', '') +
            settings.LIQPAY_PRIVATE_KEY
        )

        if request.POST.get('signature', '') == sign.decode():
            response = json.loads(base64.b64decode(request.POST.get('data')).decode())

            if response['status'] == 'success':
                try:
                    order = Orders.objects.get(id=int(response['order_id']))
                except:
                    return HttpResponse()

                payment = Payment()
                payment.order = order
                payment.amount = int(response['amount'])
                payment.comment = 'LiqPay'
                payment.token = response['liqpay_order_id']
                payment.sender_phone = response['sender_phone']
                payment.save()

                if order.get_total_price_grn() == order.get_total_paid():
                    order.paid = True
                    order.save()
                else:
                    order.paid = False
                    order.save()

                try:
                    phone = Phones.objects.get(phone=order.phone)
                    phone.active = True
                    phone.save()
                except:
                    pass

                return HttpResponse()

            else:
                try:
                    order = Orders.objects.get(id=int(response['order_id']))
                except:
                    return HttpResponse()

                order.liqpay_wait_accept = True
                order.save()
                return HttpResponse()


@csrf_exempt
def wfp_callback(request):
    if request.method == 'POST':
        config = Config.objects.get()
        raw = PaymentRaw()
        raw.data = request.body.decode('utf-8')
        raw.sign = ''
        raw.save()
        try:
            data = json.loads(raw.data)
            raw.sign = data['merchantSignature']
            raw.save()
        except:
            raise

        sign_str = ';'.join([
            data['merchantAccount'], str(data['orderReference']), str(data['amount']),
            data['currency'], str(data['authCode']), data['cardPan'],
            data['transactionStatus'], str(data['reasonCode'])
        ])

        sign = hmac.new(
            str.encode(config.merchant_secret),
            str.encode(sign_str),
            hashlib.md5
        ).hexdigest()

        if sign == raw.sign:
            response_dict = {}
            response_dict['orderReference'] = data['orderReference']
            response_dict['status'] = 'accept'
            response_dict['time'] = format(timezone.now(), 'U')
            response_dict['signature'] = ''

            response_sign_str = ';'.join([
                response_dict['orderReference'], response_dict['status'],
                str(response_dict['time'])
            ])

            response_dict['signature'] = hmac.new(
                str.encode(config.merchant_secret),
                str.encode(response_sign_str),
                hashlib.md5
            ).hexdigest()

            if data['transactionStatus'] == 'Approved':
                try:
                    order = Orders.objects.get(id=int(data['orderReference']))
                except:
                    return HttpResponse(json.dumps(response_dict, ensure_ascii=False), content_type="text/plain")

                payment = Payment()
                payment.order = order
                payment.amount = int(data['amount'])
                payment.comment = 'WayForPay'
                payment.token = data['orderReference']
                payment.sender_phone = data['phone']
                payment.save()

                if order.get_total_price_grn() == order.get_total_paid():
                    order.paid = True
                    order.liqpay_wait_accept = False
                    order.save()
                else:
                    order.paid = False
                    order.save()

                try:
                    phone = Phones.objects.get(phone=order.phone)
                    phone.active = True
                    phone.save()
                except:
                    pass

                return HttpResponse(json.dumps(response_dict, ensure_ascii=False), content_type="text/plain")

            else:
                try:
                    order = Orders.objects.get(id=int(data['orderReference']))
                except:
                    return HttpResponse(json.dumps(response_dict, ensure_ascii=False), content_type="text/plain")

                order.liqpay_wait_accept = True
                order.wfp_status = '; '.join([data['transactionStatus'], str(data['reasonCode']), data['reason']])
                order.save()
                return HttpResponse(json.dumps(response_dict, ensure_ascii=False), content_type="text/plain")
        else:
            return HttpResponse()


def messages_off(request, id):
    try:
        phone = Phones.objects.get(id=id)
        phone.news = False
        phone.save()
        message = _('You were successfully unsubscribed.')
        messages.add_message(
            request,
            messages.SUCCESS,
            message
        )

    except:
        message = _('Something went wrong. Please try later or contact us.')
        messages.add_message(
            request,
            messages.WARNING,
            message
        )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponse(json.dumps({'message': message}), content_type = 'application/json')
    else:
        return redirect('main_page')


@json_view()
def cart_valuta(request):
    valuta = request.POST.get('valuta', 'grn')

    request.session['valuta'] = valuta

    return {'success': True}
