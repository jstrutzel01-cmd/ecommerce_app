from django.test import SimpleTestCase
from django.urls import reverse, resolve
from catalog.views import product_list, product_detail #catalog functions with urls
from cart.views import cart_detail #cart functions with urls
from orders.views import order_create #orders functions with urls




class TestUrls(SimpleTestCase):

    def test_product_list_url(self):
        print("-----------Testing if product_list url works...----------- \n")
        url = reverse("product_list")
        print(resolve(url))
        #checks if url is equal to the product list
        self.assertEqual(resolve(url).func, product_list)
        print("------------Success!------------ \n")

    def test_product_detail_url(self):
        print("-----------Testing if product_detail url works...----------- \n")
        url = reverse("product_detail" , args=[1, 'slug'])
        print(resolve(url))
        #checks if url is equal to the product detail
        self.assertEqual(resolve(url).func, product_detail)
        print("------------Success!------------ \n")

    def test_cart_detail_url(self):
        print("-----------Testing if cart_detail url works...----------- \n")
        url = reverse("cart:detail" )
        print(resolve(url))
        #checks if url is equal to the cart detail
        self.assertEqual(resolve(url).func, cart_detail)
        print("------------Success!------------ \n")
    
    def test_order_create_url(self):
        print("-----------Testing if order_create url works...----------- \n")  
        url = reverse("orders:create")
        print(resolve(url))
        #checks if url is equal to the order create
        self.assertEqual(resolve(url).func, order_create)
        print("------------Success!------------ \n")
        
   

