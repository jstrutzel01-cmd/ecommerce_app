from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == "POST": # Checks if form was submitted
        form = OrderCreateForm(request.POST) # Puts form data into form variable
        if form.is_valid(): # Checks if input fields and were filled
            print(" Form is valid")
            order = form.save(commit=False)
            order.user = request.user
            order.save()
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



class OrderHistoryView(ListView):
    model = Order #Tell WHAT data will be listed
    template_name = "orders/history.html" #What is being rendered
    context_object_name = "orders"

    def get_queryset(self):         # Shows only the orders by the logged in user in descending order
        return (Order.objects
                .filter(user=self.request.user)
                .order_by("-created_at"))
    
order_history = login_required(OrderHistoryView.as_view()) # Prevents non logged in user from accessing and redirection to login. Use this for classes
