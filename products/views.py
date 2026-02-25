import json
from django.shortcuts import render
from .models import Category, Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

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

@require_POST
def receive_data(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Bad JSON"}, status=400)

    product_id = payload.get("product_id")
    

    if not product_id:
        return JsonResponse({"error": "Missing fields"}, status=400)

    return JsonResponse({"ok": True, "product_id": product_id})



@ensure_csrf_cookie
def product_page(request, slug):
    
    product = Product.objects.get(slug=slug)
    categories = Category.objects.all()

    
    return render(request, 'shopping/single.html', context={'product': product, 'categories': categories, 'page_title': product.title})


def category_filter(request, slug):
    products = Product.objects.filter(category__slug=slug)
    print(products)
    return render(request, 'shopping/category.html', context={'products': products})
