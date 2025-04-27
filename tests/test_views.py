from django.test import TestCase
from django.urls import reverse
from catalog.models import Category, Product

class CatalogViewTests(TestCase):
    """Tests for catalog.views.product_list and product_detail."""

    def setUp(self):
        # Create one category and ten products so we can exercise filters & pagination
        self.category = Category.objects.create(name="Shoes", slug="shoes")
        for i in range(10):
            Product.objects.create(
                name=f"Shoe {i}",
                slug=f"shoe-{i}",
                description="Comfortable running shoe",
                price=50,
                category=self.category,
            )
        # Convenience: pick the first product for detail-view tests
        self.product = Product.objects.first()

    # product_list

    def test_product_list_basic(self):
        print("\n-- product_list basic render --")
        url = reverse("product_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/product_list.html")
        # paginator shows 8 per page (set in view)
        self.assertEqual(len(response.context["products"]), 8)
        print("   Success!")

    def test_product_list_category_filter(self):
        print("\n-- product_list with category slug --")
        url = reverse("product_list_by_category", args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Every product returned should belong to the chosen category
        for p in response.context["products"]:
            self.assertEqual(p.category, self.category)
        print("   Success!")

    def test_product_list_search_query(self):
        print("\n-- product_list search query --")
        url = reverse("product_list") + "?q=Shoe 1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Only products whose name/description contains the query should appear
        names = [p.name for p in response.context["products"]]
        self.assertIn("Shoe 1", names)
        # A name that shouldn’t match must be absent
        self.assertNotIn("Shoe 9", names)
        print("   Success!")

    # prouct_detail

    def test_product_detail_success(self):
        print("\n-- product_detail valid id/slug --")
        url = reverse("product_detail", args=[self.product.id, self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/product_detail.html")
        self.assertEqual(response.context["product"], self.product)
        print("   Success!")

    def test_product_detail_404(self):
        print("\n-- product_detail bad slug returns 404 --")
        url = reverse("product_detail", args=[self.product.id, "wrong-slug"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        print("   Success!")