
from django.urls import path
from .views import FoodProductAPIView
from . import views
from django.urls import path

urlpatterns = [
    path('products/', FoodProductAPIView.as_view(), name='foodproduct_list'),
    path('products/<int:code>/', FoodProductAPIView.as_view(), name='foodproduct_detail'),
]