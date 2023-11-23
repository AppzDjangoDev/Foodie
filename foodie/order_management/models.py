from django.db import models
from accounts.models import *
from product_management.models import *

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    order_ref_id = models.CharField(max_length=6, unique=True, null=False, default=000000)
    customer_name = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_agent = models.ForeignKey(DeliveryAgent, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True)
    payment_mode = models.CharField(max_length=20)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    otp = models.CharField(max_length=20)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(FoodProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)