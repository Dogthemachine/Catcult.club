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

from .forms import CheckoutForm
from .models import Cart, CartItem, Orders, OrderItems
from apps.elephants.models import Balance
from apps.helpers import normalize_phone


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
            order.save()

            cart_items = CartItem.objects.filter(cart=cart)

            for item in cart_items:
                balance = Balance.objects.get(item=item.item, size=item.size)

                orderitem = OrderItems()
                orderitem.order = order
                orderitem.balance = balance
                orderitem.amount = item.amount
                orderitem.save()


            cart.delete()

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

            return {'form': False}

    t = loader.get_template('orders/cart_checkout.html')
    c = RequestContext(request, {'form': form})
    html = t.render(c)

    button_text = _('Place the order')

    return {'form': True, 'html': html, 'button_text': button_text}
