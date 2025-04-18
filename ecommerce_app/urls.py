from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView




urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("products/", include("catalog.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]
