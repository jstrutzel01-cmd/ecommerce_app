from catalog.models import Category
from cart.cart import Cart

def global_vars(request):
    return {
        "categories": Category.objects.all(),
        "cart": Cart(request),
    }
