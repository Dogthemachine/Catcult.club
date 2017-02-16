from django.conf import settings

def session_middleware(get_response):

    def middleware(request):
        request.session.save()

        request.menu_layout = settings.MENU_LAYOUT

        response = get_response(request)

        return response

    return middleware
