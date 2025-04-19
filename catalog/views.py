from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator #Paginator breaks up lists into pages if too much too is being requested
from .models import Product, Category

def product_list(request, category_slug=None):
    category = None # This line will be overrided if slug is passed
    products = Product.objects.all()
    
    if (category_slug): # Function happens if category_slug is passed
        category = Category.objects.get(slug=category_slug) # Mathches category_slug to slug in DB
        products = products.filter(category=category)
    
    paginator = Paginator(products, 8) #Creates paginator from product list to only show 8 per page
    page = request.GET.get("page", 1) #Get the current page number. Default to one
    products = paginator.get_page(page) # Now the product variable hold only the current pages 8 items

    return render(request, "catalog/product_list.html",  # Sends html template the products and the current category
                  {"products": products, "category": category},
                  )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, "catalog/product_detail.html", {"product" : product})