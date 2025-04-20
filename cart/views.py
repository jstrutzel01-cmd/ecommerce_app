from django.shortcuts import redirect, render, get_object_or_404
from catalog.models import Product
from .cart import Cart

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get("size") # Get selected from form in product_detail template
    cart.add(product=product, qty=1, size=size)          # one click = +1
    next_url = request.POST.get("next")
    return redirect(next_url) # Jumps to cart_detail view

def cart_remove(request, product_id, size):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product, size=size)
    return redirect("cart:detail")

def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})