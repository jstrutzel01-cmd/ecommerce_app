from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import OrderItem
from .forms import OrderCreateForm
from django.contrib.auth.decorators import login_required

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == "POST": # Checks if form was submitted
        form = OrderCreateForm(request.POST) # Puts form data into form variable
        if form.is_valid(): # Checks if input fields and were filled
            print(" Form is valid")
            order = form.save() # Now that form is valid store it into an order object
            for item in cart: # From __iter__() in Cart class, Loop through each item in Cart
                OrderItem.objects.create(
                    order    = order,
                    product  = item["product"],
                    price    = item["product"].price,
                    quantity = item["qty"],
                )
            cart.clear()                              # empty cart
            return render(request, "orders/created.html", {"order": order})
        else:
            print("Form not valid")
            print(form.errors)
    else:
        form = OrderCreateForm()
    return render(request, "orders/create.html", {"cart": cart, "form": form})

