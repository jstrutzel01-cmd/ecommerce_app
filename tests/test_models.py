from django.test import TestCase
from catalog.models import Product, Category

class TestModels(TestCase):
    # This sets up a temp test object to compare real object to
    def setUp(self):
        #Category object
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        #Product object
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            description="Test Description",
            price=10.00,
            category=self.category,
        )

    def test_product_creation(self):
        print("-----------Testing if Product class works...----------- \n")
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.slug, "test-product")
        self.assertEqual(self.product.description, "Test Description")
        self.assertEqual(self.product.price, 10.00)
        self.assertEqual(self.product.category, self.category)
        print("------------Success!------------ \n")

    def test_category_creation(self):
        print("-----------Testing if Category class works...----------- \n")
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.slug, "test-category")
        print("------------Success!------------ \n")
        