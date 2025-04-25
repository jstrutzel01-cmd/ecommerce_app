from django.urls import path
from . import views

app_name = "orders" # Lets us use {% 'orders:create' %}
urlpatterns = [
    path("", views.order_create, name="create"),
    path("history/", views.order_history, name="history")
]