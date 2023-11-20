from . import views
from django.urls import path
from .views import add_delivery_agent, update_delivery_agent, delivery_agent_list, customer_list, add_customer, update_customer



urlpatterns = [
    path('add_delivery_agent/', add_delivery_agent, name='add_delivery_agent'),
    path('update_delivery_agent/<str:agent_username>/', update_delivery_agent, name='update_delivery_agent'),
    path('add_customer/', add_customer, name='add_customer'),
    path('update_customer/<str:customer_username>/', update_customer, name='update_customer'),
    path('delivery_agent_list/', delivery_agent_list, name='delivery_agent_list'),
    path('customer_list/', customer_list, name='customer_list'),
]