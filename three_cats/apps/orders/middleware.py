from apps.orders.models import Cart, CartItem
from django.db.models import Sum

def info_middleware(get_response):
    def middleware(request):

        cart = Cart.objects.filter(session_key=request.session.session_key)
        request.cart_amount = 0
        if cart:
            items = CartItem.objects.filter(cart=cart[0])
            for item in items:
                request.cart_amount += item.amount - item.amount_set
            for cartset in cart[0].cartset_set.all():
                request.cart_amount += cartset.amount
        response = get_response(request)

        return response

    return middleware
