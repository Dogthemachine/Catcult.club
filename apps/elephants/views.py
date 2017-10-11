from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
from django.utils import timezone

from .forms import AddToCartForm, SetSizesForm
from .models import Photo, Categories, Fashions, Items, Sizes, Sets, Balance, SetsPhoto, Stocks
from apps.orders.models import Cart, CartItem, CartSet, CartSetItem
from apps.info.models import Info


def showcase(request, category_id=None, fashion_id=None):
    #print(request.LANGUAGE_CODE)
    category = None
    fashion = None
    items = None

    if category_id:
        category = get_object_or_404(Categories, id=category_id)

    if fashion_id:
        fashion = get_object_or_404(Fashions, id=fashion_id)

    categories = Categories.objects.all()

    fashions = None

    if category and fashion:
        fashions = Fashions.objects.filter(categories=category, displayed=True)
        items = Items.objects.filter(fashions=fashion)
        sets = []

    elif category:
        if category.set:
            sets = Sets.objects.filter(categories=category)
            items = []
        else:
            items = Items.objects.filter(fashions__categories=category)
            sets = []
        fashions = Fashions.objects.filter(categories=category, displayed=True)

    else:
        items = Items.objects.all()
        sets = Sets.objects.all()

    avail_items = []
    not_avail_items = []
    new_items = []

    for item in items:
        for balance in item.balance_set.all():
            if balance.amount > 0:
                item.is_set = False
                if datetime(item.added.year, item.added.month, item.added.day) < datetime.today()-timedelta(days=15):
                    avail_items.append(item)
                else:
                    new_items.append(item)
                break

    for item in items:
        amount = []

        for balance in item.balance_set.all():
            if balance.amount == 0:
                amount.append(balance)

        if len(amount) == item.balance_set.count():
            item.is_set = False
            not_avail_items.append(item)

    if sets:
        for set in sets:
            i = Items.objects.filter(sets=set)
            res = False
            if i:
                res = True
            for item in i:
                balances = Balance.objects.filter(item=item)
                am = False
                for balance in balances:
                    if balance.amount > 0:
                        am = True
                res = res and am
            if res:
                set.is_set = True
                avail_items.append(set)
            else:
                set.is_set = True
                not_avail_items.append(set)

    avail_items.sort(key=lambda x: x.views, reverse=True)

    not_avail_items.sort(key=lambda x: x.views, reverse=True)

    items = new_items + avail_items + not_avail_items

    paginator = Paginator(items, 12)

    page = request.GET.get('page')

    try:
        itm = paginator.page(page)
    except PageNotAnInteger:
        itm = paginator.page(1)
    except EmptyPage:
        itm = paginator.page(paginator.num_pages)

    return render(request,
                  'elephants/showcase.html',
                  {'category': category,
                   'categories': categories,
                   'fashion': fashion,
                   'fashions': fashions,
                   'items': items,
                   'itm': itm})


def item_details(request, id):
    item = get_object_or_404(Items, id=id)

    photos = Photo.objects.filter(item=item).order_by('added')

    sizes = Sizes.objects.select_related().filter(balance__item=item, balance__amount__gt=0).count()

    if sizes > 0:
        form = AddToCartForm(item=item)
    else:
        form = None

    if request.method == 'POST':
        form = AddToCartForm(request.POST, item=item)
        if form.is_valid():
            cart, cart_created = Cart.objects.get_or_create(session_key=request.session.session_key)
            cart.session = request.session.session_key
            cart.save()

            cart_item = CartItem.objects.filter(cart=cart, item=item, size=form.cleaned_data['size'])
            if cart_item:
                cart_item = cart_item[0]
                cart_item.amount += form.cleaned_data['quantity']
            else:
                cart_item = CartItem(
                    cart = cart,
                    item = item,
                    size = form.cleaned_data['size'],
                    amount = form.cleaned_data['quantity']
                )
            cart_item.save()

            action = cart.get_items_count()
            if action:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _('%(name)s was added to your cart. %(count)s') % {'name': item.name, 'count': action}
                )
            else:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _('%(name)s was added to your cart.') % {'name': item.name}
                )

            request.cart_amount += cart_item.amount

            return redirect('item_details', id=item.id)
    else:
        item.views_today = item.views_today + 1
        item.save()

    return render(request,
                  'elephants/item_details.html',
                  {'photos': photos, 'item': item, 'form': form})


def item_set_details(request, id):
    set = get_object_or_404(Sets, id=id)

    photos = SetsPhoto.objects.filter(set=set).order_by('added')

    items = Items.objects.filter(sets=set)

    res = False
    if items:
        res = True

    for item in items:
        balances = Balance.objects.filter(item=item)
        am = False
        for balance in balances:
            if balance.amount > 0:
                am = True
        res = res and am

    if res:
        form = SetSizesForm(set=set)
    else:
        form = None

    if request.method == 'POST':
        form = SetSizesForm(request.POST, set=set)
        if form.is_valid():
            cart, cart_created = Cart.objects.get_or_create(session_key=request.session.session_key)
            cart.session = request.session.session_key
            cart.save()

            cartset = CartSet()
            cartset.cart = cart
            cartset.set = set
            cartset.amount = form.cleaned_data['quantity']
            cartset.save()

            for name, value in form.cleaned_data.items():
                if name.startswith('item_'):
                    cart_item = CartItem.objects.filter(cart=cart, item=form.fields[name].item, size=form.cleaned_data[name])
                    if cart_item:
                        cart_item = cart_item[0]
                        cart_item.amount += form.cleaned_data['quantity']
                        cart_item.amount_set += form.cleaned_data['quantity']
                    else:
                        cart_item = CartItem(
                            cart = cart,
                            item = form.fields[name].item,
                            size = form.cleaned_data[name],
                            amount = form.cleaned_data['quantity'],
                            amount_set = form.cleaned_data['quantity']
                        )
                    cart_item.save()

                    cartsetitem = CartSetItem()
                    cartsetitem.cartset = cartset
                    cartsetitem.item = form.fields[name].item
                    cartsetitem.size = form.cleaned_data[name]
                    cartsetitem.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                _('%(name)s was added to your cart. %(count)s') % {'name': set.name, 'count': cart.get_items_count()}
            )

            request.cart_amount += form.cleaned_data['quantity']

            return redirect('item_set_details', id=set.id)
    else:
        set.views_today = set.views_today + 1
        set.save()

    return render(request,
                  'elephants/item_set_details.html',
                  {'photos': photos, 'set': set, 'form': form})


def stocks(request):
    stocks = Stocks.objects.filter(action_end__gte=timezone.datetime.today()-timedelta(days=365)).order_by('-id')

    topic = get_object_or_404(Info, topic='stocks')

    return render(request, 'elephants/stocks.html', {'topic': topic, 'stocks': stocks})

