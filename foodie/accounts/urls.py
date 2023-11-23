from django.urls import path
from .views import DeliveryAgentListView, DeliveryAgentDetailView, CustomerListView, CustomerDetailView, CustomLoginView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('delivery_agents/', DeliveryAgentListView.as_view(), name='delivery-agent-list'),
    path('delivery_agents/<str:user__username>/', DeliveryAgentDetailView.as_view(), name='delivery-agent-detail'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customers/<str:user__username>/', CustomerDetailView.as_view(), name='customer-detail'),

]