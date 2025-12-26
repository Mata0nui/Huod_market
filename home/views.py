from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Welcome " + username + "!"))
            return redirect('home')
        else:
            messages.success(request, ("There Was An Error login In, Try Again..."))
            return redirect('login')
    
    else:
        return render(request, 'members/login.html', context={'page_title': 'Login'})

def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged out!"))
    return redirect('home')

# TODO: Добавить email в форму регистрации

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successfull!"))
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'members/register_user.html', {
        'form':form,
    }, context={'page_title': 'Register'})



def checkout_page(request):
    return render(request, 'shopping/cheackout.html', context={'page_title': 'Checkout'})

def cart_page(request):
    return render(request, 'shopping/cart.html', context={'page_title': 'Shopping Cart'})

def bestseller_page(request):
    return render(request, 'shopping/bestseller.html', context={'page_title': 'Bestsellers'})

def single_page(request):
    return render(request, 'shopping/single.html', context={'page_title': 'Single Product'})

def error_404_page(request):
    return render(request, 'shopping/404.html', status=404)

def profile_page(request):
    return render(request, 'members/profile.html', context={'page_title': 'User Profile'})