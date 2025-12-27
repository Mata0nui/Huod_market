from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

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

def profile_page(request):
    return render(request, 'members/profile.html', context={'page_title': 'User Profile'})