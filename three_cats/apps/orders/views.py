# -*- coding: utf-8 -*-
import base64
import json
from jsonview.decorators import json_view

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext, loader, Context
from django.utils.translation import ugettext as _
from django.db.models import Sum
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.urls import reverse

from .forms import CheckoutForm
from .models import Cart, CartItem, Orders, OrderItems, Payment, PaymentRaw
from apps.liqpay import LiqPay
from apps.elephants.models import Balance
from apps.helpers import normalize_phone, send_sms


@json_view
def cart(request):
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    cart.session = request.session.session_key
    cart.save()

    if not created:
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart_items = []

    t = loader.get_template('orders/cart.html')
    c = RequestContext(request, {'cart': cart, 'cart_items': cart_items})
    html = t.render(c)

    return {'html': html}


@json_view
def cart_remove(request, id):
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)

    if not created:
        try:
            cart_item = CartItem.objects.get(id=id)
        except CartItem.DoesNotExist:
            return {'success': False}
        else:
            cart_item.delete()
            cart_items = CartItem.objects.filter(cart=cart)
    else:
        return {'success': False}

    t = loader.get_template('orders/cart.html')
    c = RequestContext(request, {'cart': cart, 'cart_items': cart_items})
    html = t.render(c)

    return {'html': html, 'count': cart_items.count()}


@json_view
def cart_checkout(request):
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)

    if created:
        return {'success': False}

    form = CheckoutForm()

    no_avail_items = 0

    cart_items = CartItem.objects.filter(cart=cart)

    for item in cart_items:
        if not item.check_avail():
            no_avail_items += 1

    if no_avail_items:

        t = loader.get_template('orders/cart.html')
        c = RequestContext(request, {'cart': cart, 'cart_items': cart_items})
        html = t.render(c)

        return {'form': False, 'html': html}

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Orders()
            order.name = form.cleaned_data['name']
            order.phone = normalize_phone(form.cleaned_data['phone'])
            order.lang_code = request.LANGUAGE_CODE
            order.payment_method = form.cleaned_data['payment']
            order.delivery_method = form.cleaned_data['delivery']
            order.user_comment = form.cleaned_data['comment']
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

            cart.delete()

            if order.payment_method == 2:
                if order.lang_code == 'en':
                    text = 'Your order %(number)s has been taken. Card number is %(card)s (%(name)s) and sum is %(sum)s. CatCult' % {'number': order.get_number, 'card': settings.PRIVAT_CARD, 'name': settings.PRIVAT_NAME, 'sum': order.get_total_price()}
                elif order.lang_code == 'ru':
                    text = 'Ваш заказ %(number)s был принят. Номер карты %(card)s (%(name)s). Сумма к оплате %(sum)s грн. CatCult' % {'number': order.get_number, 'card': settings.PRIVAT_CARD, 'name': settings.PRIVAT_NAME, 'sum': order.get_total_price()}
                else:
                    text = ''

                send_sms(order.phone, text)

            else:
                if order.lang_code == 'en':
                    text = 'Your order %(number)s has been taken. Total price is %(sum)s. CatCult' % {'number': order.get_number, 'sum': order.get_total_price()}
                elif order.lang_code == 'ru':
                    text = 'Ваш заказ %(number)s был принят. Сумма к оплате %(sum)s. CatCult' % {'number': order.get_number, 'sum': order.get_total_price()}
                else:
                    text = ''

                send_sms(order.phone, text)

            message = _('Your order has been placed. We will contact you shortly.<br/>Order details:<br/>')
            message += order.name + '<br/>' + str(order.phone) + '<br/>'
            for item in order.orderitems_set.all():
                message += item.balance.item.name + ' - '
                message += item.balance.size.name + ' - '
                message += str(item.amount) + '<br/>'
                message += _('Total:') + ' ' + str(order.get_total_price()) + ' ' + _('UAH') + '<br/>'

            messages.add_message(
                request,
                messages.SUCCESS,
                message
            )

            if order.payment_method == 3:
                liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
                payment_form = liqpay.cnb_form({
                    'action': 'pay',
                    'amount': order.get_total_price(),
                    'currency': 'UAH',
                    'description': 'CatCult order',
                    'order_id': order.id,
                    'server_url': settings.LIQPAY_CALLBACK,
                    'result_url': settings.LIQPAY_SUCCESS
                })

                return {'payment_form': payment_form}

            return {'form': False}

    t = loader.get_template('orders/cart_checkout.html')
    c = RequestContext(request, {'form': form})
    html = t.render(c)

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

                if order.get_total_price() == order.get_total_paid():
                    order.paid = True
                    order.save()
                else:
                    order.paid = False
                    order.save()

                return HttpResponse()

            else:
                try:
                    order = Orders.objects.get(id=int(response['order_id']))
                except:
                    return HttpResponse()

                order.liqpay_wait_accept = True
                order.save()
                return HttpResponse()
