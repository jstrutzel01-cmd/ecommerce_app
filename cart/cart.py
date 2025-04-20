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
    def add(self, product, qty=1, override=False, size=None):
        product_id = str(product.id) # keys in session must be strings
        key = f"{product_id}-{size}" if size else product_id # We cannot use product_id for adding items to cart becuse adding a new iterm with the same size will override the old one
        
        if key not in self.cart:
            self.cart[key] = {"qty": 0, "price": str(product.price), "size": size}
        if override:
            self.cart[key]["qty"] = qty
        else:
            self.cart[key]["qty"] += qty
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
    def __iter__(self): #this function prepares all the cart data so template can extract whatever it data it wants from each object. __iter__ is called when for loop uses cart
        for key, item in self.cart.items():
            product_id = key.split("-")[0]  # get just the ID from '6-XS'
            product = Product.objects.get(id=product_id)  # gets the product from DB

            item = item.copy() # Makes a copy of the cart item so it can be modified for the display, but not mess with saved session data
            item["product"] = product # Adds the actual name from Prodcut Object
            item["total_price"] = Decimal(item["price"]) * item["qty"]
            yield item

    def __len__(self):
        return sum(item["qty"] for item in self.cart.values())

    def get_total_price(self):
        from decimal import Decimal
        return sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())

    def save(self):
        self.session.modified = True
