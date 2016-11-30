from apps.orders.models import Cart, CartItem
from django.db.models import Sum

def info_middleware(get_response):
    def middleware(request):

        cart = Cart.objects.filter(session_key=request.session.session_key)
        request.cart_amount = 0
        items = CartItem.objects.filter(cart=cart)
        for item in items:
            request.cart_amount += item.amount
        response = get_response(request)

        return response

    return middleware
