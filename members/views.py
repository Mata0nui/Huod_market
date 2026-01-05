from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from .form import *
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Welcome " + username + "!"))
            return redirect('home')
        else:
            messages.success(request, ("There Was An Error login In, Try Again..."))
    return render(request, 'members/login.html', context={'page_title': 'Login'})

def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged out!"))
    return redirect('home')

# TODO: Добавить email в форму регистрации

def register_user(request):
    if request.method == "POST":
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, ("Registration Successfull!"))
            return redirect('home')
    else:
        form = RegistrationUserForm()
    return render(request, 'members/register_user.html', {
        'form':form,
    'page_title': 'Register'})

@login_required
def profile_edit_page(request):
    user = request.User

def profile_page(request):
    return render(request, 'members/profile.html', context={'page_title': 'User Profile'})