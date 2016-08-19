from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from apps.info.models import Maintitle, Info
from apps.elephants.models import Stores

def main_page(request):

    if request.user.is_authenticated():

        return render_to_response('main_page/main_page_mod.html', {
                                                                  },
                                  context_instance=RequestContext(request))

    else:

        mainpage = get_object_or_404(Info, topic='mainpage')

        try:
            items = Stores.objects.all()
            maintitle = Maintitle.objects.all()
        except:
            raise

        return render_to_response('main_page/main_page.html', {'mainpage': mainpage,
                                                               'items': items,
                                                               'maintitle': maintitle},
                                  context_instance=RequestContext(request))


def construction_page(request):

        return render_to_response('main_page/construction_page.html', {
                                                               },
                                  context_instance=RequestContext(request))
