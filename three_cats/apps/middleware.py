def session_middleware(get_response):

    def middleware(request):
        request.session.save()

        response = get_response(request)

        return response

    return middleware
