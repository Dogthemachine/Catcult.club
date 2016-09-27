def session_middleware(get_response):

    def middleware(request):
        try:
            session_key = request.session.session_key
        except:
            request.session.create()

        response = get_response(request)

        return response

    return middleware
