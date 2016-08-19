import json

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from apps.elephants.models import Items


@login_required(login_url='/login/')
@permission_required('info.delete_info', login_url='/login/')
def items(request, id):

    items = Items.objects.filter(fashions__id=id)

    if len(items) == 0:
        items = [{'name': _('There is no items now')}]

    return render_to_response('moderation/items.html', {'items': items},
                              context_instance=RequestContext(request))