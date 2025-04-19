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
        self.session = request.session # Accesses session data
        cart = self.session.get("cart") # Gets "cart" from session if there is one from a previous session. "cart" is created from add
        if cart is None:
            cart = self.session["cart"] = {} # Crete empty cart if none
        self.cart = cart

    # --- core API ---
    def add(self, product, qty=1, override=False):
        product_id = str(product.id) # keys in session must be strings
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
        product_ids = self.cart.keys() # keys() returns a view of all the keys in that dictionary
        products = Product.objects.filter(id__in=product_ids) #Use id__in to filter all ids in cart
        for p in products:
            item = self.cart[str(p.id)]
            item["product"] = p
            item["total_price"] = Decimal(item["price"]) * item["qty"]
            yield item # Return one item at a time

    def __len__(self):
        return sum(item["qty"] for item in self.cart.values())

    def get_total_price(self):
        from decimal import Decimal
        return sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())

    def save(self):
        self.session.modified = True
