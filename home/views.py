from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm



def checkout_page(request):
    return render(request, 'shopping/cheackout.html', context={'page_title': 'Checkout'})

def cart_page(request):
    return render(request, 'shopping/cart.html', context={'page_title': 'Shopping Cart'})

def bestseller_page(request):
    return render(request, 'shopping/bestseller.html', context={'page_title': 'Bestsellers'})


def error_404_page(request):
    return render(request, 'shopping/404.html', status=404, context={'page_title': 'Упс...'})

