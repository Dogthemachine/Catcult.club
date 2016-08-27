import json
from jsonview.decorators import json_view
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.db.models import Count

from .models import Cart, Orders, Orderitems
from ..elephants.models import Items


@json_view
@csrf_exempt
def elephants_order(request, id, amount):

    if request.method == 'POST':

        item = get_object_or_404(Items, id=id)

        try:
            session_key = request.session.session_key
        except:
            request.session.create()
            session_key = request.session.session_key

        b = Cart(item=item, session_key=session_key, amount=amount)
        b.save()

        messages.add_message(request, messages.SUCCESS, _(u'Added to cart: %s') % item.name)

    return {'success': True}


@csrf_exempt
def cart(request):

    try:
        cart = Cart.objects.select_related().filter(session_key=request.session.session_key)
    except:
        raise Http404


    html = render_to_string('elephants/cart.html',
                                {'cart': cart},
                                context_instance=RequestContext(request))

    response_data = {'html': html}

    return HttpResponse(json.dumps(response_data),
                            mimetype="application/json")


@json_view
def cart_remove(request, id):

    if request.method == 'POST':

        try:
            Cart.objects.get(id=id).delete()
        except:
            raise

    return {'success': True}


def orders(request, status=None, id=None):

    if not request.user.is_authenticated():
        return redirect('/')

    orders = Orders.objects.filter(status=0).count()

    status_select = [{'name': _('All status'), 'id': 4}]
    for status_position in settings.ORDER_STATUS:
        status_select = status_select + [{'name': _(status_position[1]), 'id': status_position[0]}]

    if status:
        if id:
            order = get_object_or_404(Orders, id=id)
            order.status = status
            order.save()
        tab_orders = Orders.objects.all().filter(status=status)
        status_name = _(settings.ORDER_STATUS[int(status)][1])
    else:
        tab_orders = Orders.objects.all()
        status_name = _('All status')

    i = 0
    for tab_orders_item in tab_orders:
        tab_orders[i].status_name = _(settings.ORDER_STATUS[int(tab_orders_item.status)][1])
        i = i + 1

    return render_to_response('elephants/orders.html', {'tab_orders': tab_orders,
                                                        'status_name': status_name,
                                                        'status_select': status_select,
                                                        'orders': orders},
                              context_instance=RequestContext(request))


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

