from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils import timezone

from apps.elephants.models import Sizes, Categories, Stocks, Items
from apps.info.models import Config
from apps.orders.views import price_description

register = template.Library()


@register.simple_tag
def get_size_desc(size_id):
    try:
        size = Sizes.objects.get(id=size_id)
    except:
        return ''

    return size.description


@register.simple_tag
def get_item_img(item_id):
    try:
        item = Items.objects.get(id=item_id)
    except:
        return ''

    return mark_safe('<img class="img-responsive" src="%s">' % item.image_small.url)


@register.simple_tag
def get_categories(request):
    try:
        categories = Categories.objects.all().order_by('sequence')
        m = ''
        for category in categories:
            m = m + '<li class="nav-item"><a class="nav-link cc-main-menu-color" href="/%s/showcase/%i/" title="%s">%s</a></li>' \
                    % (request.LANGUAGE_CODE, category.id, _(category.name), _(category.name))

    except:
        return ''

    return mark_safe(m)


@register.simple_tag
def get_price(entry, request):
    price = entry.price
    discount_price = entry.get_actual_price()
    if request.session['valuta'] == 'grn':
        if price == discount_price:
            html = '%s' % entry.get_actual_price()
        else:
            name = entry.get_discount_name()
            html = '<span class="icon-info cc-tooltip" data-toggle="tooltip" data-original-title="%s"></span>' % name
            html += ' <del>%s</del> %s' % (price, discount_price)
    else:
        config = Config.objects.get()
        rate = 1
        if request.session['valuta'] == 'usd':
            rate = config.dollar_rate
        if request.session['valuta'] == 'eur':
            rate = config.euro_rate
        price = round(price / rate, 2)
        discount_price = round(discount_price / rate, 2)
        if price == discount_price:
            html = '%s' % price
        else:
            name = entry.get_discount_name()
            html = '<span class="icon-info cc-tooltip" data-toggle="tooltip" data-original-title="%s"></span>' % name
            html += ' <del>%s</del> %s' % (price, discount_price)

    return mark_safe(html)


@register.simple_tag
def get_price_description(request):
    html = price_description(request)
    return mark_safe(html)


@register.simple_tag
def get_total(cart, request):
    total = cart.get_total()
    if request.session['valuta'] == 'grn':
        html = '%s' % total
    else:
        config = Config.objects.get()
        rate = 1
        if request.session['valuta'] == 'usd':
            rate = config.dollar_rate
        if request.session['valuta'] == 'eur':
            rate = config.euro_rate
        total = round(total / rate, 2)
        html = '%s' % total

    return mark_safe(html)


@register.simple_tag
def get_stocks():
    m=''
    """
    try:
        global_stock = Stocks.objects.filter(action_begin__lte=timezone.datetime.today(),
                                             action_end__gte=timezone.datetime.today()).order_by('-id')
        if global_stock:
            st = '<div id="marquee">%s' % (_('Action!!!')) + ' '
            for gs in global_stock:
                st = st + '%s' % (_(gs.name)) + ' '
            m = st + '</div>'

    except:
        return mark_safe('')
    """

    return mark_safe(m)


@register.filter
def subtract(value, arg):
    return value - arg