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
from .models import Cart, CartItem, Orders, Orderitems
from apps.elephants.models import Balance


@json_view
def cart(request):
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    cart.session = request.session.session_key
    cart.save()

    if not created:
        cart_items = CartItem.objects.filter(cart=cart)

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

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Orders()
            order.name = form.cleaned_data['name']
            order.phone = form.cleaned_data['phone']
            order.save()

            cart_items = CartItem.objects.filter(cart=cart)

            for item in cart_items:
                balance = Balance.objects.get(item=item.item, size=item.size)

                orderitem = Orderitems()
                orderitem.order = order
                orderitem.balance = balance
                orderitem.amount = item.amount
                orderitem.save()


            cart.delete()

            messages.add_message(
                request,
                messages.SUCCESS,
                _('Your order has been placed. We will contact you shortly.')
            )

            return {'form': False}

    t = loader.get_template('orders/cart_checkout.html')
    c = RequestContext(request, {'form': form})
    html = t.render(c)

    button_text = _('Place the order')

    return {'form': True, 'html': html, 'button_text': button_text}


def orders(request, status=None):

    if not request.user.is_authenticated():
        return redirect('/')


    status_select = [{'name': _('All status'), 'id': 4}]
    for status_position in settings.ORDER_STATUS:
        status_select = status_select + [{'name': _(status_position[1]), 'id': status_position[0]}]

    if status:
        orders = Orders.objects.filter(status=status).count()
        status_name = _(settings.ORDER_STATUS[int(status)][1])
    else:
        orders = Orders.objects.all()
        status_name = _('All status')

    i = 0
    for order in orders:
        order[i].status_name = _(settings.ORDER_STATUS[int(order.status)][1])
        i = i + 1

    return render_to_response('elephants/orders.html', {'status_name': status_name,
                                                        'status_select': status_select,
                                                        'orders': orders},
                              context_instance=RequestContext(request))


@json_view
@csrf_exempt
def elephants_order(request, id):

    if request.method == 'POST':

        item = get_object_or_404(Balance, id=id)

        try:
            session_key = request.session.session_key
        except:
            request.session.create()
            session_key = request.session.session_key

        b = Cart(balance=item, session_key=session_key)
        b.save()

        messages.add_message(request, messages.SUCCESS, _(u'Added to cart: %s') % item.item.name)

    return {'success': True}






def order_position(request):

    if request.is_ajax():

        order_id = request.GET.get('order_id', 0)

        order = get_object_or_404(Orders, id=order_id)
        items = Orderitems.objects.filter(order=order)
        delivery = settings.DELIVERY[int(order.delivery)][1]
        payment = settings.PAYMENT[int(order.payment)][1]

        html = render_to_string('elephants/order_position.html',
                                {'order': order, 'items': items, 'delivery': delivery, 'payment': payment},
                                context_instance=RequestContext(request))

        response_data = {'html': html}

        return HttpResponse(json.dumps(response_data),
                        mimetype="application/json")

    else:
        raise PermissionDenied()
