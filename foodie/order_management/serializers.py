# serializers.py
from rest_framework import serializers

class OrderItemSerializer(serializers.Serializer):
    product_code = serializers.CharField()
    quantity = serializers.IntegerField()

class CreateOrderSerializer(serializers.Serializer):
    product_items = OrderItemSerializer(many=True)
    payment_mode = serializers.CharField()

