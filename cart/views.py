from django.shortcuts import redirect, render, get_object_or_404
from catalog.models import Product
from .cart import Cart

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, qty=1)          # one click = +1
    return redirect("cart:detail") # Jumps to cart_detail view

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:detail")

def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})