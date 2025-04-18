from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class Category(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)} # Slug autofills as you type category name
    list_display = ("name",) # In list view, show name column

@admin.register(Product)
class Product(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name",)