# from django.urls import path
# from .views import create_order


# urlpatterns = [
#     path('create_order/', create_order, name='create_order'),

# ]
# urls.py
from django.urls import path
from .views import OrderListCreateView, OrderRetrieveUpdateDestroyView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<slug:order_ref_id>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-retrieve-update-destroy'),
]