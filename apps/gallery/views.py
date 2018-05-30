from jsonview.decorators import json_view
from django.template import loader

from django.shortcuts import get_object_or_404, render

from .models import Gallery


def gallery_photo(request, id):

    gallery = get_object_or_404(Gallery, id=id)

    return render(request, 'gallery/gallery_photo.html', {'gallery': gallery})


def gallery(request):

    gallery = Gallery.objects.all().order_by('-added')

    return render(request, 'gallery/gallery.html', {'gallery': gallery})


@json_view
def gallery_photo_mod(request, id):

    gallery = get_object_or_404(Gallery, id=id)

    t = loader.get_template('gallery/gallery_photo.html')
    c = {'gallery': gallery}
    html = t.render(c, request)

    return {'html': html}