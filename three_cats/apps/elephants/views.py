from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from .models import Photo, Categories, Fashions, Items


def showcase(request, category_id, fashion_id):

    categories = Categories.objects.all()
    if fashion_id > 0:
        items = Items.objects.filter(fashions__id=fashion_id)
    else:
        if category_id > 0:
            items = Items.objects.filter(fashions__categories__id=category_id)
        else:
            items = Items.objects.all()


    return render_to_response('elephants/showcase.html', {'categories': categories,
                                                          'category_id': category_id,
                                                          'fashion_id': fashion_id,
                                                          'items': items},
                              context_instance=RequestContext(request))


def item_details(request, id):

    photos = Photo.objects.filter(item__id=id).order_by('added')
    item = get_object_or_404(Items, id=id)

    try:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()

    except:
        request.session.create()

        photos = Photo.objects.filter(item=item)

    if len(photos) == 0:
        photos = [{'name': _('There is no potos of this image now')}]

    return render_to_response('elephants/item_details.html', {'photos': photos,
                                                              'item': item},
                              context_instance=RequestContext(request))

