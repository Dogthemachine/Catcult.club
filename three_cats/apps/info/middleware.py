class UserProfileMiddleware(object):
    """

    Set `request.cart_amount` to correspondent profile type.

    """
    def process_request(self, request):
        from django.db.models import Sum
        from apps.orders.models import Cart, Orders

        if request.user.is_authenticated():
            request.cart_amount = None
            request.new_orders = Orders.objects.filter(status=0).count()

        else:
            #request.cart_amount = Cart.objects.filter(session_key=request.session._session_key).aggregate(Sum('amount'))
            request.cart_amount = 10
            request.new_orders = None

        return None
