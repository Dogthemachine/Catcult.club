# -*- coding: utf-8 -*-
from jsonview.decorators import json_view
import csv
import json
import datetime

from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader, Context
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db.models import Sum

from apps.helpers import send_sms
from apps.elephants.models import Balance, Items, BalanceLog, Categories
from apps.orders.models import Orders, OrderItems, Payment, Phones, IWant
from apps.comments.models import Comments
from .forms import OrderForm, CommentForm, DeliveryForm, PaymentForm
from .models import LastOrdersCheck

from .decorators import user_is_admin


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def balances(request):
    items = Items.objects.all()

    return render(request, 'moderation/balances.html', {'items': items})


@json_view
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def balances_update(request):
    if request.method == 'POST':
        try:
            id = int(request.POST.get('id', None))
            amount = int(request.POST.get('amount', None))
            arrival = bool(request.POST.get('arrival', None))
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

                return {'success': True, 'message': _('Balance was saved. Old value: %(old)s, new value: %(new)s') % {'old': log.old_value, 'new': log.new_value}}


        else:
            return {'success': False, 'message': _('Error')}


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
@user_is_admin()
def log(request):
    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)
    arrival = request.GET.get('arrival', None)
    if arrival == 'true':
        arrival = 'True'
    else:
        arrival = 'False'

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
        change_time__date__lte=datetime.date(date_to[0], date_to[1], date_to[2]),
        arrival=arrival
    )

    date_from = '-'.join(list(map(str, date_from)))
    date_to = '-'.join(list(map(str, date_to)))

    return render(request, 'moderation/log.html', {'logs': logs, 'date_from': date_from, 'date_to': date_to, 'arrival': arrival})


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
def manage_iwant(request):

    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)
    status = request.GET.get('status', 100)
    filter_status = status

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
        if int(status) > 0:
            iwant = IWant.objects.filter(
                added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
                added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2]),
                status=status
            ).order_by('-added')
        else:
            iwant = IWant.objects.filter(
                added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
                added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
            ).order_by('-added')
    else:
        iwant = IWant.objects.filter(status=status).order_by('-added')

    date_from = '-'.join(list(map(str, date_from)))
    date_to = '-'.join(list(map(str, date_to)))

    status = [{'name': 'All', 'val': 0}]
    for stat in IWant.STATUS:
        status.append({'name': stat[1], 'val': stat[0]})

    return render(request, 'moderation/i_want.html', {
        'status': status, 'iwant': iwant, 'date_from': date_from, 'date_to': date_to,
        'max_status': max(IWant.STATUS)[0], 'filter_status': int(filter_status),
    })


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def manage_comments(request):

    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)
    status = request.GET.get('status', 0)
    filter_status = status

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
        if int(status) > 0:
            comments = Comments.objects.filter(
                added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
                added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2]),
                status=status
            ).order_by('-added')
        else:
            comments = Comments.objects.filter(
                added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
                added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
            ).order_by('-added')
    else:
        comments = Comments.objects.all().order_by('-added')

    date_from = '-'.join(list(map(str, date_from)))
    date_to = '-'.join(list(map(str, date_to)))

    status = [{'name': 'All', 'val': 0}]
    for stat in Comments.STATUS:
        status.append({'name': stat[1], 'val': stat[0]})

    return render(request, 'moderation/comments.html', {
        'status': status, 'comments': comments, 'date_from': date_from, 'date_to': date_to,
        'max_status': max(Comments.STATUS)[0], 'filter_status': int(filter_status),
    })



@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def manage_orders(request):
    last, created = LastOrdersCheck.objects.get_or_create(id=1)
    orderitems = OrderItems.objects.filter(order__added__gte=last.datetime, balance__amount=0)
    if orderitems:
        message = _('The stock is out of stock:')
        for orderitem in orderitems:
            message += ' ' + _('Item') + ' - ' + orderitem.balance.item.name + '   '
            message += _('Size') + ' - ' + orderitem.balance.size.name + ';'
        messages.add_message(
            request,
            messages.WARNING,
            message
        )
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
                if order.lang_code == 'en':
                    text = 'Your order #%(number)s has been sent. TTN: %(ttn)s. CatCult' % {'number': order.get_number(), 'ttn': order.ttn}
                elif order.lang_code == 'ru':
                    text = 'Ваш заказ №%(number)s был отправлен. ТТН: %(ttn)s. CatCult' % {'number': order.get_number(), 'ttn': order.ttn}
                elif order.lang_code == 'uk':
                    text = 'Ваше замовлення №%(number)s було відправлено. ТТН: %(ttn)s. CatCult' % {'number': order.get_number(), 'ttn': order.ttn}
                else:
                    text = ''

                send_sms(order.phone, text)
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
    iwant = IWant.objects.filter(status=IWant.NEW).count()
    comm = Comments.objects.filter(status=Comments.NEW).count()
    if orders:
        new_order = True
    else:
        new_order = False
    if iwant:
        iwant_new = True
    else:
        iwant_new = False
    if comm:
        comm_new = True
    else:
        comm_new = False
    return {'new': new_order, 'count': orders, 'iwant_count': iwant, 'iwant': iwant_new,
            'comm_count': comm, 'comm': comm_new}


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
    c = {'order': order}
    html = t.render(c, request)

    t = loader.get_template('moderation/j_order_info_buttons.html')
    c = {'order': order}
    buttons = t.render(c, request)

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
    c = {'form': form}
    html = t.render(c, request)

    t = loader.get_template('moderation/j_order_comment_buttons.html')
    c = {'order': order}
    buttons = t.render(c, request)

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

        t = loader.get_template('moderation/j_order_delivery_success.html')
        c = {'order': order}
        html = t.render(c, request)

        return {'success': True, 'html': html}

    title = _('Delivery')

    form_date = order.date_of_delivery if order.date_of_delivery else datetime.date.today()

    form = DeliveryForm(initial={'delivery': order.delivery_method, 'ttn': order.ttn, 'date': form_date})
    t = loader.get_template('moderation/j_order_delivery.html')
    c = {'form': form, 'order': order}
    html = t.render(c, request)

    t = loader.get_template('moderation/j_order_delivery_buttons.html')
    c = {'order': order}
    buttons = t.render(c, request)

    if request.method == 'POST' and reset == False:
        form = DeliveryForm(request.POST)
        if form.is_valid():
            order.delivery_method = form.cleaned_data.get('delivery')
            order.ttn = form.cleaned_data.get('ttn', 0)
            order.date_of_delivery = form.cleaned_data.get('date', None)
            order.save()

            if order.ttn > 0 and not order.sms_sent:
                if order.lang_code == 'en':
                    text = 'Your order #%(number)s has been sent. TTN: %(ttn)s. CatCult' % {'number': order.get_number(), 'ttn': order.ttn}
                elif order.lang_code == 'ru':
                    text = 'Ваш заказ №%(number)s был отправлен. ТТН: %(ttn)s. CatCult' % {'number': order.get_number(), 'ttn': order.ttn}
                elif order.lang_code == 'uk':
                    text = 'Ваше замовлення №%(number)s було відправлено. ТТН: %(ttn)s. CatCult' % {'number': order.get_number(), 'ttn': order.ttn}
                else:
                    text = ''

                send_sms(order.phone, text)
                order.sms_sent = True
                order.save()

            if order.date_of_delivery:
                order.delivered = True
                order.save()
            else:
                order.delivered = False
                order.save()

            t = loader.get_template('moderation/j_order_delivery_success.html')
            c = {'order': order}
            html = t.render(c, request)

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
    c = {'form': form, 'order': order}
    html = t.render(c, request)

    t = loader.get_template('moderation/j_order_payment_buttons.html')
    c = {'order': order}
    buttons = t.render(c, request)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = Payment()
            payment.order = order
            payment.amount = form.cleaned_data.get('amount')
            payment.comment = form.cleaned_data.get('comment', '')
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

            t = loader.get_template('moderation/j_order_payment_success.html')
            c = {'order': order}
            html = t.render(c, request)

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
    c = {'order': payment.order}
    html = t.render(c, request)

    form = PaymentForm(initial={'amount': payment.order.get_remaining_amount})
    t = loader.get_template('moderation/j_order_payment.html')
    c = {'order': payment.order, 'form': form}
    modal_html = t.render(c, request)

    t = loader.get_template('moderation/j_order_payment_buttons.html')
    c = {'order': payment.order}
    buttons = t.render(c, request)

    return {'success': True, 'html': html, 'modal_html': modal_html, 'buttons': buttons}


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def j_order_packed(request, id):
    try:
        order = Orders.objects.get(id=id)
    except:
        return {'success': False}

    if request.method == 'POST':
        order.packed = True
        order.save()

        t = loader.get_template('moderation/j_order_delivery_success.html')
        c = {'order': order}
        html = t.render(c, request)

        return {'success': True, 'html': html}


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

        t = loader.get_template('moderation/items.html')
        c = {'order': order}
        html = t.render(c, request)

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
        order_item.price = balance.item.get_actual_price()
        try:
            order_item.amount = int(request.POST.get('amount', None))
        except:
            raise
            return {'success': False, 'message': _('Something went wrong.')}
        order_item.save()

        return {'success': True}


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def iwant_change_status(request, order_id):
    try:
        iwant = IWant.objects.get(id=order_id)
    except:
        return {'success': False, 'message': _('Something went wrong.')}
    else:
        try:
            status = int(request.POST.get('status', None))
            iwant.status = status
        except:
            raise
            return {'success': False, 'message': _('Something went wrong.')}
        iwant.save()

        return {'success': True}


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def iwant_delete(request, order_id):
    try:
        iwant = IWant.objects.get(id=order_id)
        iwant.delete()
        return {'success': True}
    except:
        return {'success': False, 'message': _('Something went wrong.')}


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def iwant_change_comment(request, order_id):
    try:
        iwant = IWant.objects.get(id=order_id)
    except:
        return {'success': False, 'message': _('Something went wrong.')}
    else:
        try:
            comment = request.POST.get('comment', None)
            iwant.comment = comment
        except:
            raise
            return {'success': False, 'message': _('Something went wrong.')}
        iwant.save()

        return {'success': True}


@json_view()
@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def comment_change_status(request, comment_id):
    status = int(request.POST.get('status', None))
    if not status:
        return {'success': False, 'message': _('Something went wrong.')}
    try:
        comment = Comments.objects.get(id=comment_id)
    except:
        return {'success': False, 'message': _('Something went wrong.')}
    else:
        try:
            comment.status = status
        except:
            raise
            return {'success': False, 'message': _('Something went wrong.')}
        comment.save()

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
def order_info(request, id):

    html = loader.get_template('moderation/order_info.html')

    return {'html': html}


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
@user_is_admin()
def stat_sale(request):
    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)
    payment = int(request.GET.get('payment', -1))

    if date_from:
        date_from = list(map(int, date_from.split('-')))
    else:
        date_from = list(map(int, datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days=30), '%Y-%m-%d').split('-')))

    if date_to:
        date_to = list(map(int, date_to.split('-')))
    else:
        date_to = list(map(int, datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d').split('-')))

    stat = Categories.objects.all()
    for category in stat:
        if payment == -1:
            category.amount = OrderItems.objects.filter(
                added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
                added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2]),
                balance__item__fashions__categories=category).aggregate(total_amount=Sum('amount'))['total_amount']
            items = OrderItems.objects.filter(
                added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
                added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2]),
                balance__item__fashions__categories=category).all()
        else:
            category.amount = OrderItems.objects.filter(order__payment_method=payment,
                added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
                added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2]),
                balance__item__fashions__categories=category).aggregate(total_amount=Sum('amount'))['total_amount']
            items = OrderItems.objects.filter(order__payment_method=payment,
                added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
                added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2]),
                balance__item__fashions__categories=category).all()
        category.sum = 0
        category_profit = 0
        for item in items:
            category.sum = category.sum + item.amount * item.price
            category_profit = category_profit + item.amount * item.balance.item.fashions.cost_price
        category.profit = category.sum - category_profit

    if payment == -1:
        total_orders = Orders.objects.filter(
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        ).count()
    else:
        total_orders = Orders.objects.filter(payment_method=payment,
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        ).count()

    if payment == -1:
        total_payments = Payment.objects.filter(
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        ).aggregate(total_sum=Sum('amount'))
    else:
        total_payments = Payment.objects.filter(order__payment_method=payment,
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        ).aggregate(total_sum=Sum('amount'))

    if payment == -1:
        items = OrderItems.objects.filter(
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        ).all()
    else:
        items = OrderItems.objects.filter(order__payment_method=payment,
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        ).all()

    totat_amount = 0
    for item in items:
        totat_amount += item.amount * item.price

    totat_profit = 0
    for item in items:
        totat_profit += item.amount * item.balance.item.fashions.cost_price
    totat_profit = totat_amount - totat_profit

    if payment == -1:
        items = OrderItems.objects.filter(
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        ).exclude(order__discount_promo=0).all()
    else:
        items = OrderItems.objects.filter(order__payment_method=payment,
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        ).exclude(order__discount_promo=0).all()
    total_discount_promo = 0
    for item in items:
        total_discount_promo += int(item.amount*item.price*item.order.discount_promo/100)

    if payment == -1:
        total_discount_stocks = Orders.objects.filter(
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        ).aggregate(total_sum=Sum('discount_stocks'))

        orders = Orders.objects.filter(
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        ).all()
    else:
        total_discount_stocks = Orders.objects.filter(payment_method=payment,
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        ).aggregate(total_sum=Sum('discount_stocks'))

        orders = Orders.objects.filter(payment_method=payment,
            added__date__gte=datetime.date(date_from[0], date_from[1], date_from[2]),
            added__date__lte=datetime.date(date_to[0], date_to[1], date_to[2])
        ).all()

    total_discount_set = 0
    for order in orders:
        total_discount_set += order.discount_set

    date_from = '-'.join(list(map(str, date_from)))
    date_to = '-'.join(list(map(str, date_to)))

    return render(request, 'moderation/stat_sale.html', {'stat': stat, 'date_from': date_from, 'date_to': date_to,
                                                         'total_orders': total_orders,
                                                         'total_amount': totat_amount,
                                                         'total_profit': totat_profit,
                                                         'total_payments': total_payments['total_sum'],
                                                         'total_discount_promo': total_discount_promo,
                                                         'total_discount_stocks': total_discount_stocks['total_sum'],
                                                         'total_discount_set': total_discount_set},
                  )


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
@user_is_admin()
def stat_ending(request, rest=0):

    balances = Balance.objects.filter(amount=rest)
    for balance in balances:
        order_items = OrderItems.objects.filter(balance=balance).order_by('-added')[:1]
        for order_item in order_items:
            balance.ld = order_item.added
            date_from = order_item.added - datetime.timedelta(days=30)

        balance.sl = OrderItems.objects.filter(balance=balance, added__gte=date_from).count()

    return render(request, 'moderation/stat_ending.html', {
        'balances': balances
                                                           },
                  )


@json_view()
def stat_payment(request):
    payment = request.POST.get('payment', -1)

    request.session['payment'] = payment

    return {'success': True}
