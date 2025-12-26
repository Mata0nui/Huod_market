from django.urls import path, re_path
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
    path('', shop_page, name='home'),
    path('<slug:slug>/', product_page, name='product_detail'),
]