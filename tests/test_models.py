from django.test import TestCase
from catalog.models import Product, Category
from orders.models import Order, OrderItem
from django.contrib.auth.models import User


class TestModels(TestCase):
    # This sets up a temp test object to compare real object to
    def setUp(self):
        #Category object
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        #Product object
        self.product1 = Product.objects.create(
            name="White T-Shirt",
            slug="test-product1",
            description="Test Description",
            price=10.00,
            category=self.category,
        )

         # Create a test user first
        self.test_user = User.objects.create_user(
            username='defaultuser',
            email='default@example.com',
            password='defaultpassword123'
        )


        #Order object
        self.order = Order.objects.create(
            user=self.test_user,
            first_name='Allen',
            last_name='Iversom',
            email='AI@gmail.com',
            shipping_address='131 No Rings </3',
            city='Philadelphia',
        )

        #OrderItem object
        self.order_item = OrderItem.objects.create(
            order=self.order,  # This will be set later when creating the Order
            product=self.product1,
            price=self.product1.price,
            quantity=3,
        )

    def test_product_creation(self):
        print("-----------Testing if Product class works...----------- \n")
        self.assertEqual(self.product1.name, "White T-Shirt")
        self.assertEqual(self.product1.slug, "test-product1")
        self.assertEqual(self.product1.description, "Test Description")
        self.assertEqual(self.product1.price, 10.00)
        self.assertEqual(self.product1.category, self.category)
        print("------------Success!------------ \n")

    def test_category_creation(self):
        print("-----------Testing if Category class works...----------- \n")
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.slug, "test-category")
        print("------------Success!------------ \n")

    def test_order_item_price(self):
        print("-----------Testing if OrderItem class works as well as get_cost()...-----------")
        self.assertEqual(self.order_item.product, self.product1)
        self.assertEqual(self.order_item.price, 10.00)
        self.assertEqual(self.order_item.quantity, 3)
        #Gets total cost of order item with 3 total items at 10.00 each
        print("OrderItem cost: ", self.order_item.get_cost())
        self.assertEqual(self.order_item.get_cost(), 30.00)
        print("3 items: ", self.order_item.get_cost()," = 30.00")
        print("------------Success!------------ \n")
        