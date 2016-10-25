from django.template import RequestContext
from django.shortcuts import get_object_or_404, render

from apps.info.models import Carousel, Info, Stores


def main_page(request):
    if request.user.is_authenticated():
        return render(request, 'main_page/main_page_mod.html', {})

    else:
        mainpage = get_object_or_404(Info, topic='mainpage')
        delivery = get_object_or_404(Info, topic='delivery')
        payment = get_object_or_404(Info, topic='payment')

        items = Stores.objects.all()
        carousel = Carousel.objects.all()

        return render(request, 'main_page/main_page.html', {
            'mainpage': mainpage, 'items': items, 'carousel': carousel,
            'delivery': delivery, 'payment': payment
        })
