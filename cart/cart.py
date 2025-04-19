# cart/cart.py
from decimal import Decimal
from django.conf import settings
from catalog.models import Product

class Cart:
    """
    A session‑stored cart accessible as Cart(request).
    Uses request.session["cart"] = {<product_id>: {"qty": 1, "price": "19.99"}, …}
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if cart is None:
            cart = self.session["cart"] = {}
        self.cart = cart

    # --- core API ---
    def add(self, product, qty=1, override=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"qty": 0, "price": str(product.price)}
        if override:
            self.cart[product_id]["qty"] = qty
        else:
            self.cart[product_id]["qty"] += qty
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session.pop("cart", None)
        self.session.modified = True

    # --- helpers ---
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for p in products:
            item = self.cart[str(p.id)]
            item["product"] = p
            item["total_price"] = Decimal(item["price"]) * item["qty"]
            yield item

    def __len__(self):
        return sum(item["qty"] for item in self.cart.values())

    def get_total_price(self):
        from decimal import Decimal
        return sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())

    def save(self):
        self.session.modified = True
