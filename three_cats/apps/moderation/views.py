from jsonview.decorators import json_view
import json
import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils.translation import ugettext as _

from apps.elephants.models import Balance, Items, BalanceLog


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

        if id and amount:
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
    print(date_from, date_to)

    date_from = '-'.join(list(map(str, date_from)))
    date_to = '-'.join(list(map(str, date_to)))
    print(date_from, date_to)

    return render(request, 'moderation/log.html', {'logs': logs, 'date_from': date_from, 'date_to': date_to})
