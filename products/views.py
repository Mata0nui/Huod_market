from django.shortcuts import render
from .models import Category, Product

# Create your views here.
def shop_page(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', context={'products': products})

def product_page(request, slug):
    
    product = Product.objects.get(slug=slug)
    
    return render(request, 'shop/product_detail.html', context={'product': product})
    