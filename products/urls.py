from django.urls import path, re_path
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
    path('', shop_page, name='home'),
    path('product/<slug:slug>/', product_page, name='product_detail'),
    path('category/<slug:slug>/', category_filter, name='category_filter'),
]