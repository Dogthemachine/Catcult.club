from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from .forms import AddToCartForm
from .models import Photo, Categories, Fashions, Items, Sizes
from apps.orders.models import Cart, CartItem


def showcase(request, category_id=None, fashion_id=None):
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

    elif category:
        items = Items.objects.filter(fashions__categories=category)
        fashions = Fashions.objects.filter(categories=category, displayed=True)

    else:
        items = Items.objects.all()

    avail_items = []
    not_avail_items = []

    for item in items:
        for balance in item.balance_set.all():
            if balance.amount > 0:
                avail_items.append(item)
                break

    for item in items:
        amount = []

        for balance in item.balance_set.all():
            if balance.amount == 0:
                amount.append(balance)

        if len(amount) == item.balance_set.count():
            not_avail_items.append(item)

    items = avail_items + not_avail_items

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

            cart_item = CartItem(
                cart = cart,
                item = item,
                size = form.cleaned_data['size'],
                amount = form.cleaned_data['quantity']
            )
            cart_item.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                _('%s was added to your cart.') % item.name
            )

            request.cart_amount += 1

            return redirect('item_details', id=item.id)
    else:
        item.views_today = item.views + 1
        item.save()

    return render(request,
                  'elephants/item_details.html',
                  {'photos': photos, 'item': item, 'form': form})
