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
from ..elephants.models import Balance


def cart(request):

    try:
        cart = Cart.objects.select_related('balance__item').filter(session_key=request.session.session_key)
    except:
        raise Http404

    return render_to_response('orders/cart.html', {'cart': cart
                                                   },
                              context_instance=RequestContext(request))


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


@json_view
def cart_remove(request, id):

    if request.method == 'POST':

        try:
            Cart.objects.get(id=id).delete()
        except:
            raise

    return {'success': True}

