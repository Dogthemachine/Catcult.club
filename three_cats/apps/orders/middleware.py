from apps.orders.models import Cart, CartItem

def info_middleware(get_response):
    def middleware(request):

        cart = Cart.objects.filter(session_key=request.session.session_key)
        request.cart_amount = CartItem.objects.filter(cart=cart).count()

        response = get_response(request)

        return response

    return middleware
