from django.shortcuts import render
from .models import Category, Product

# Create your views here.

def shop_page(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    try:
        category = request.GET.get('category_r')
    except ValueError:
        pass
    if category:
        products = Product.objects.filter(category__slug=category)


    return render(request, 'shopping/shop.html', context={'c': category_filter, 'products': products, 'page_title': 'Home', 'categories': categories})

def product_page(request, slug):
    
    product = Product.objects.get(slug=slug)
    categories = Category.objects.all()

    return render(request, 'shopping/single.html', context={'product': product, 'categories': categories, 'page_title': product.title})

def category_filter(request, slug):
    products = Product.objects.filter(category__slug=slug)
    print(products)
    return render(request, 'shopping/category.html', context={'products': products})
