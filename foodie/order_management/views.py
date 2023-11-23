import random
import string
from product_management.models import FoodProduct
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderItemSerializer

def generate_order_ref_id():
    while True:
        # Generate the remaining six characters (numbers)
        order_ref_gen = ''.join(random.choices(string.digits, k=6))
        # Check if the order_ref_id already exists in the Order table
        if not Order.objects.filter(order_ref_id=order_ref_gen).exists():
            return order_ref_gen

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_data = serializer.validated_data
        product_items = order_data['product_items']
        payment_mode = order_data['payment_mode']

        unique_order_ref_id = generate_order_ref_id()
        order = Order.objects.create(order_ref_id=unique_order_ref_id, order_status='pending', payment_mode=payment_mode)

        total_price = 0
        total_charges = 0

        for item_data in product_items:
            print("item_dataitem_dataitem_data", item_data)
            product_code = item_data['product_code']  # Change this line
            quantity = item_data['quantity']
            product = FoodProduct.objects.get(product_code=product_code)

            item_charge = product.product_charge
            total_charges += item_charge

            item_price = product.price * quantity
            total_price += item_price

            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=item_price)

        order.order_total = total_price + total_charges
        order.total_charges = total_charges
        order.save()

        return Response({'order_id': order.order_ref_id, 'message': 'Your order has been created successfully.', 'amount_paid': order.order_total}, status=status.HTTP_201_CREATED)

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
    lookup_field = 'order_ref_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        order_data = serializer.validated_data
        product_items = order_data['product_items']
        payment_mode = order_data['payment_mode']

        instance.payment_mode = payment_mode
        instance.save()

        # Delete existing order items
        OrderItem.objects.filter(order=instance).delete()

        total_price = 0
        for item_data in product_items:
            product_code = item_data['product']['product_code']
            quantity = item_data['quantity']
            product = FoodProduct.objects.get(product_code=product_code)

            item_price = product.price * quantity
            total_price += item_price

            OrderItem.objects.create(order=instance, product=product, quantity=quantity, price=item_price)

        instance.order_total = total_price
        instance.save()

        return Response({'order_id': instance.order_ref_id, 'message': 'Your order has been updated successfully.', 'amount_paid': instance.order_total})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
