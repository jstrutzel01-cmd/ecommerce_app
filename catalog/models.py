from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"] # Category objects will be sorted alphabetically when listed
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product_detail", args=[self.id, self.slug]) #Returns the URL for a page that shows all products in this category


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="products/",blank=True)
    created_at = models.DateField(auto_now_add=True) #Creates data field only when instance is created
    updated_at = models.DateField(auto_now=True) #Updates the date field after save
    GENDER_CHOICES = [
        ("M", "Men"),
        ("W", "Women"),
        ("U", "Unisex"),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="U")

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["id", "slug"])] #Creates a database index on id and slug for fast lookup

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product_detail", args=[self.id, self.slug]) #Returns the URL for a page that shows all products in this category