from .models import CartItem, Cart
from .views import _cart_id

def counter(request):
    cart_counter = 0

    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
        cart_items = CartItem.objects.filter(cart=cart)

        for item in cart_items:
            cart_counter += item.quantity
    except Cart.DoesNotExist:
        pass
    return dict(cart_count=cart_counter)