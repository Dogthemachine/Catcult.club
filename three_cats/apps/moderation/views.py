import json
import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from apps.elephants.models import Balance, Items
from apps.moderation.models import Corrections


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def balances(request):

    items = Items.objects.all()

    return render_to_response('moderation/balances.html', {'items': items},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def advent(request):

    return render_to_response('moderation/advent.html', {'items': ''},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def correction(request):


    date_from = datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days=30), '%d-%m-%Y')
    date_from_code = datetime.date.today() - datetime.timedelta(days=30)

    try:
        correction = Corrections.objects.get(added__gt=date_from_code)
    except:
        correction = None

    return render_to_response('moderation/correction.html',
                              {'date_from': date_from,
                               'employee_manager': correction
                              },
                              context_instance=RequestContext(request))