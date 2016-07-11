from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from apps.elephants.models import (Item, Cart, Orders)
from apps.info.models import Maintitle, Info

def main_page(request):

    mainpage = get_object_or_404(Info, topic='mainpage')

    try:
        items = Item.objects.select_related('stores').order_by("-added")
        maintitle = Maintitle.objects.all()
        orders = Orders.objects.filter(status=0).count()
        cart = Cart.objects.filter(session_key=request.session._session_key).aggregate(Sum('amount'))
    except:
        raise

    if len(items) == 0:
        items = [{'name': _('There is no images now')}]

    return render_to_response('main_page/main_page.html', {'main_page': True,
                                                           'mainpage': mainpage,
                                                           'items': items,
                                                           'orders': orders,
                                                           'maintitle': maintitle,
                                                           'cart': cart},
                              context_instance=RequestContext(request))
