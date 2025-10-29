from django.urls import path
from .views import *

urlpatterns = [
    path('', shop_page, name='shop_page_link'),
    path('<slug:slug>/', product_page, name='product_detail')
    
]