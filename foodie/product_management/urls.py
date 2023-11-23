# urls.py
from django.urls import path
from .views import FoodProductListCreateView, FoodProductRetrieveUpdateDestroyView

urlpatterns = [
    path('products/', FoodProductListCreateView.as_view(), name='product-list-create'),
    path('products/<str:product_code>/', FoodProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),
]
