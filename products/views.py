import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from .models import Category, Product, Cart
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

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
@login_required
def receive_data(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (ValueError, TypeError):
        return JsonResponse({"error": "Bad JSON"}, status=400)

    product_id = payload.get("product_id")
    product_quantity = payload.get("product_quantity")

    if product_id is None or product_quantity is None:
        return JsonResponse({"error": "Missing fields"}, status=400)

    try:
        product_quantity = int(product_quantity)
        if product_quantity <= 0:
            return JsonResponse({"error": "Quantity must be > 0"}, status=400)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid quantity"}, status=400)

    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": product_quantity},
    )

    return JsonResponse({
        "ok": True,
        "cart_id": cart.id,
        "created": created,
        "product_id": product.id,
        "product_quantity": cart.quantity,
    })



@ensure_csrf_cookie
def product_page(request, slug):
    
    product = Product.objects.get(slug=slug)
    categories = Category.objects.all()

    
    return render(request, 'shopping/single.html', context={'product': product, 'categories': categories, 'page_title': product.title})


def category_filter(request, slug):
    products = Product.objects.filter(category__slug=slug)
    print(products)
    return render(request, 'shopping/category.html', context={'products': products})


@login_required
def cart_page(request):
    carts = Cart.objects.select_related("product").filter(user=request.user)
    categories = Category.objects.all()

    cart_items = []
    cart_total = Decimal("0.00")
    for cart in carts:
        line_total = cart.product.price * cart.quantity
        cart_items.append({"cart": cart, "line_total": line_total})
        cart_total += line_total

    return render(
        request,
        "shopping/cart.html",
        context={
            "carts": carts,
            "cart_items": cart_items,
            "cart_total": cart_total,
            "status": carts.exists(),
            "categories": categories,
            "page_title": "Shopping Cart",
        },
    )

@require_POST
@login_required
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return redirect("cart_page")


@require_POST
@login_required
def pay_cart(request):
    with transaction.atomic():
        user_model = get_user_model()
        user = user_model.objects.select_for_update().get(pk=request.user.pk)
        carts = (
            Cart.objects.select_for_update()
            .select_related("product")
            .filter(user=user)
        )

        if not carts.exists():
            messages.warning(request, "Cart is empty.", extra_tags="cart")
            return redirect("cart_page")

        cart_total = Decimal("0.00")
        for cart in carts:
            cart_total += cart.product.price * cart.quantity
            product = cart.product
            product.quantity -= cart.quantity
            product.save(update_fields=["quantity"])

        total_to_pay = cart_total.quantize(Decimal("0.01"))
        current_balance = Decimal(user.balance or 0).quantize(Decimal("0.01"))

        if current_balance < total_to_pay:
            messages.error(
                request,
                f"Payment failed: not enough balance ({current_balance} UAH, need {total_to_pay} UAH).",
                extra_tags="cart",
            )
            return redirect("cart_page")

        user.balance = current_balance - total_to_pay
        user.save(update_fields=["balance"])
        carts.delete()

    messages.success(
        request,
        f"Payment successful. Charged {total_to_pay} UAH.",
        extra_tags="cart",
    )
    return redirect("checkout")

