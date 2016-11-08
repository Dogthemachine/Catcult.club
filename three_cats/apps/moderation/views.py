from jsonview.decorators import json_view
import csv
import json
import datetime

from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext, loader, Context
from django.utils import timezone
from django.utils.translation import ugettext as _

from apps.helpers import send_sms
from apps.elephants.models import Balance, Items, BalanceLog
from apps.orders.models import Orders, OrderItems, Payment
from .forms import OrderForm, CommentForm, DeliveryForm, PaymentForm
from .models import LastOrdersCheck


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def balances(request):
    items = Items.objects.all()

    return render(request, 'moderation/balances.html', {'items': items})


@json_view
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def balances_update(request, arrival):
    if request.method == 'POST':
        try:
            id = int(request.POST.get('id', None))
            amount = int(request.POST.get('amount', None))
        except:
            return {'success': False, 'message': _('Error')}

        if id and amount >= 0:
            try:
                balance = Balance.objects.get(id=id)

            except Balance.DoesNotExist:
                return {'success': False, 'message': _('Error: no balance.')}

            else:
                old_amount = balance.amount

                balance.amount = amount
                balance.save()

                log = BalanceLog()
                log.balance = balance
                log.old_value = old_amount
                log.new_value = amount
                if arrival:
                    log.arrival = True
                log.user = request.user
                log.save()

                return {'success': True, 'message': _('Balance was saved. Old value: %s, new value: %s') % (log.old_value, log.new_value)}


        else:
            return {'success': False, 'message': _('Error')}


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def arrival(request):
    items = Items.objects.all()

    return render(request, 'moderation/arrival.html', {'items': items})


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def log(request):
    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)

    if date_from:
        date_from = list(map(int, date_from.split('-')))
    else:
        date_from = list(map(int, datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days=30), '%Y-%m-%d').split('-')))


    if date_to:
        date_to = list(map(int, date_to.split('-')))
    else:
        date_to = list(map(int, datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d').split('-')))

    logs = BalanceLog.objects.filter(
        change_time__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
        change_time__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
    )

    date_from = '-'.join(list(map(str, date_from)))
    date_to = '-'.join(list(map(str, date_to)))

    return render(request, 'moderation/log.html', {'logs': logs, 'date_from': date_from, 'date_to': date_to})


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def export_balance(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="catcult-balance-%s.csv"' % datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')

    writer = csv.writer(response)
    writer.writerow([_('Category'), _('Fashion'), _('Item'), _('Size'), _('Balance')])

    for balance in Balance.objects.all().order_by('item'):
        writer.writerow([balance.item.fashions.categories, balance.item.fashions, balance.item, balance.size, balance.amount])

    return response


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def manage_orders(request):
    last, created = LastOrdersCheck.objects.get_or_create(id=1)
    last.save()

    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)

    show_archived = False

    if date_from or date_to:
        show_archived = True

    if date_from:
        date_from = list(map(int, date_from.split('-')))
    else:
        date_from = list(map(int, datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days=30), '%Y-%m-%d').split('-')))


    if date_to:
        date_to = list(map(int, date_to.split('-')))
    else:
        date_to = list(map(int, datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d').split('-')))

    if show_archived:
        orders = Orders.objects.filter(
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        )
    else:
        orders = Orders.objects.exclude(delivered=True, paid=True)

    date_from = '-'.join(list(map(str, date_from)))
    date_to = '-'.join(list(map(str, date_to)))

    return render(request, 'moderation/orders.html', {
        'orders': orders, 'date_from': date_from, 'date_to': date_to
    })


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def delete_order(request, id):
    order = get_object_or_404(Orders, id=id)

    order.delete()

    messages.add_message(
        request,
        messages.SUCCESS,
        _('Order %s was deleted.') % id
    )

    return redirect('orders')


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def manage_order(request, id):
    order = get_object_or_404(Orders, id=id)

    order_items = OrderItems.objects.filter(order=order)

    all_items = Items.objects.select_related().all()

    items = []

    for item in all_items:
        for balance in item.balance_set.all():
            if balance.amount > 0:
                items.append(item)
                break

    if request.method == 'POST':
        order_form = OrderForm(request.POST, instance=order)
        if order_form.is_valid():
            order_form.save()

            if order.ttn > 0 and not order.sms_sent:
                text = r'TTN: %(ttn)s. CatCult'
                context = {'ttn': order.ttn}
                send_sms(order.phone, text, context)
                order.sms_sent = True
                order.save()
    else:
        order_form = OrderForm(instance=order)


    return render(request, 'moderation/order.html', {
        'order': order, 'order_form': order_form, 'order_items': order_items,
        'items': items
    })


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def check_orders(request):
    last, created = LastOrdersCheck.objects.get_or_create(id=1)
    orders = Orders.objects.filter(added__gte=last.datetime).count()
    if orders:
        return {'new': True, 'count': orders}
    else:
        return {'new': False}


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def j_order_info(request, id):
    try:
        order = Orders.objects.get(id=id)
    except:
        return {'success': False}

    title = _('Order info')

    t = loader.get_template('moderation/j_order_info.html')
    c = RequestContext(request, {'order': order})
    html = t.render(c)

    t = loader.get_template('moderation/j_order_info_buttons.html')
    c = RequestContext(request, {'order': order})
    buttons = t.render(c)

    return {'success': True, 'title': title, 'html': html, 'buttons': buttons}


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def j_order_delete(request, id):
    try:
        order = Orders.objects.get(id=id)
    except:
        return {'success': False}

    order.delete()

    return {'success': True}


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def j_order_comment(request, id):
    try:
        order = Orders.objects.get(id=id)
    except:
        return {'success': False}

    title = _('Comment')

    form = CommentForm(initial={'comment': order.comment})
    t = loader.get_template('moderation/j_order_comment.html')
    c = RequestContext(request, {'form': form})
    html = t.render(c)

    t = loader.get_template('moderation/j_order_comment_buttons.html')
    c = RequestContext(request, {'order': order})
    buttons = t.render(c)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            order.comment = form.cleaned_data.get('comment', '')
            order.save()

            return {'success': True, 'html': order.comment}

    return {'success': True, 'title': title, 'html': html, 'buttons': buttons}


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def j_order_delivery(request, id, reset=False):
    try:
        order = Orders.objects.get(id=id)
    except:
        return {'success': False}

    if request.method == 'POST' and reset == True:
        order.delivered = False
        order.date_of_delivery = None
        order.ttn = 0
        order.save()

    title = _('Delivery')

    form_date = order.date_of_delivery if order.date_of_delivery else datetime.date.today()

    form = DeliveryForm(initial={'delivery': order.delivery_method, 'ttn': order.ttn, 'date': form_date})
    t = loader.get_template('moderation/j_order_delivery.html')
    c = RequestContext(request, {'form': form, 'order': order})
    html = t.render(c)

    t = loader.get_template('moderation/j_order_delivery_buttons.html')
    c = RequestContext(request, {'order': order})
    buttons = t.render(c)

    if request.method == 'POST' and reset == False:
        form = DeliveryForm(request.POST)
        if form.is_valid():
            order.delivery_method = form.cleaned_data.get('delivery')
            order.ttn = form.cleaned_data.get('ttn', 0)
            order.date_of_delivery = form.cleaned_data.get('date', None)
            order.save()

            if order.ttn > 0 and not order.sms_sent:
                text = r'TTN: %(ttn)s. CatCult'
                context = {'ttn': order.ttn}
                send_sms(order.phone, text, context)
                order.sms_sent = True
                order.save()

            if order.date_of_delivery:
                order.delivered = True
                order.save()
            else:
                order.delivered = False
                order.save()

            t = loader.get_template('moderation/j_order_delivery_success.html')
            c = RequestContext(request, {'order': order})
            html = t.render(c)

            return {'success': True, 'html': html}

        else:
            return {'success': False, 'html': html}

    return {'success': True, 'title': title, 'html': html, 'buttons': buttons}


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def j_order_payment(request, id):
    try:
        order = Orders.objects.get(id=id)
    except:
        return {'success': False}

    title = _('Payment')

    form = PaymentForm(initial={'amount': order.get_remaining_amount})
    t = loader.get_template('moderation/j_order_payment.html')
    c = RequestContext(request, {'form': form, 'order': order})
    html = t.render(c)

    t = loader.get_template('moderation/j_order_payment_buttons.html')
    c = RequestContext(request, {'order': order})
    buttons = t.render(c)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = Payment()
            payment.order = order
            payment.amount = form.cleaned_data.get('amount')
            payment.comment = form.cleaned_data.get('comment', '')
            payment.save()

            if order.get_total_price() == order.get_total_paid():
                order.paid = True
                order.save()
            else:
                order.paid = False
                order.save()

            t = loader.get_template('moderation/j_order_payment_success.html')
            c = RequestContext(request, {'order': order})
            html = t.render(c)

            return {'success': True, 'html': html}

        else:
            return {'success': False, 'html': html}

    return {'success': True, 'title': title, 'html': html, 'buttons': buttons}



@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def j_order_payment_delete(request, id):
    try:
        payment = Payment.objects.get(id=id)
    except:
        return {'success': False}

    payment.delete()

    if payment.order.get_total_price() == payment.order.get_total_paid():
        payment.order.paid = True
        payment.order.save()
    else:
        payment.order.paid = False
        payment.order.save()

    t = loader.get_template('moderation/j_order_payment_success.html')
    c = RequestContext(request, {'order': payment.order})
    html = t.render(c)

    form = PaymentForm(initial={'amount': payment.order.get_remaining_amount})
    t = loader.get_template('moderation/j_order_payment.html')
    c = RequestContext(request, {'order': payment.order, 'form': form})
    modal_html = t.render(c)

    t = loader.get_template('moderation/j_order_payment_buttons.html')
    c = RequestContext(request, {'order': payment.order})
    buttons = t.render(c)

    return {'success': True, 'html': html, 'modal_html': modal_html, 'buttons': buttons}


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def delete_order_item(request, id, item_id):
    try:
        order = Orders.objects.get(id=id)
        item = OrderItems.objects.get(id=item_id)
    except:
        return {'success': False, 'message': _('Something went wrong.')}
    else:
        item.delete()

        items = OrderItems.objects.filter(order=order)

        t = loader.get_template('moderation/items.html')
        c = RequestContext(request, {'order': order})
        html = t.render(c)

        return {'success': True, 'html': html}


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def add_order_item(request, id, balance_id):
    try:
        order = Orders.objects.get(id=id)
        balance = Balance.objects.get(id=balance_id)
    except:
        return {'success': False, 'message': _('Something went wrong.')}
    else:
        order_item = OrderItems()
        order_item.order = order
        order_item.balance = balance
        try:
            order_item.amount = int(request.POST.get('amount', None))
        except:
            raise
            return {'success': False, 'message': _('Something went wrong.')}
        order_item.save()

        return {'success': True}


@json_view
def order_comment(request, id):

    html = loader.get_template('moderation/order_comment.html')

    return {'html': html}


@json_view
def order_delivery(request, id):

    html = loader.get_template('moderation/order_delivery.html')

    return {'html': html}


@json_view
def order_payment(request, id):

    html = loader.get_template('moderation/order_payment.html')

    return {'html': html}


@json_view
def order_info(request, id):

    html = loader.get_template('moderation/order_info.html')

    return {'html': html}
