from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"] # Category objects will be sorted alphabetically when listed

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product_detail", args=[self.id, self.slug]) #Returns the URL for a page that shows all products in this category

