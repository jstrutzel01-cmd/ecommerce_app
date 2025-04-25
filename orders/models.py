from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    shipping_address = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    paid = models.BooleanField(default=False)
    created_at =models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"] #Shows order list in descending order

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name = "order_items", on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_cost(self):
        return self.price * self.quantity