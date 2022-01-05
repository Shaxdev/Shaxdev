from orders.models import WishlistModel, CartModel
from django.contrib.auth.decorators import login_required



def universal_objects(request):
    if request.user.is_authenticated:
        wishlist__objects = WishlistModel.objects.filter(user=request.user)
        cart__objects = CartModel.objects.filter(user=request.user)
        context = {
            'wishlist__objects': wishlist__objects,
            'cart__objects': cart__objects,
        }
        return context
   