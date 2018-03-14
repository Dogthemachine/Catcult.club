from django.shortcuts import get_object_or_404, render

from .models import Gallery


def gallery_photo(request, id):

    gallery = get_object_or_404(Gallery, id=id)

    return render(request, 'gallery/gallery_photo.html', {'gallery': gallery})


def gallery(request):

    gallery = Gallery.objects.all().order_by('-added')

    return render(request, 'gallery/gallery.html', {'gallery': gallery})