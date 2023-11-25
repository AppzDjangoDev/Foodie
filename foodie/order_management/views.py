from datetime import timezone
import random
import string
from accounts.models import Customer, DeliveryAgent, User
from product_management.models import FoodProduct
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderItemSerializer, OrderSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from rest_framework.permissions import IsAdminUser

def generate_order_ref_id():
    latest_order = Order.objects.order_by('-order_ref_id').first()
    if latest_order:
        order_ref_gen=int(latest_order.order_ref_id)+1
    else:
        order_ref_gen=1000
    return order_ref_gen

def otp_generator():
    while True:
        otp_gen = ''.join(random.choices(string.digits, k=6))
        if not Order.objects.filter(otp=otp_gen).exists():
            return otp_gen

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            orders = self.get_queryset()
        elif hasattr(user, 'deliveryagent'):
            delivery_agent = user.deliveryagent
            orders = Order.objects.filter(delivery_agent=delivery_agent)
        elif hasattr(user, 'customer'):
            customer = user.customer
            orders = Order.objects.filter(customer_name=customer)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # try:
        user = self.request.user
        customer = Customer.objects.get(user=user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_data = serializer.validated_data
        product_items = order_data['product_items']
        payment_mode = order_data['payment_mode']

        unique_order_ref_id = generate_order_ref_id()
        order = Order.objects.create(customer_name=customer, order_ref_id=unique_order_ref_id, order_status='pending', payment_mode=payment_mode)

        total_price = 0
        total_charges = 0

        print("pppppppppppppppp")

        for item_data in product_items:

            print("item_data", item_data)
            product_code = item_data['product_code']
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

        self.send_order_confirmation_email(order, user)

        return Response({'order_id': order.order_ref_id, 'message': 'Your order has been created successfully.', 'amount_paid': order.order_total},
                            status=status.HTTP_201_CREATED)
        # except Exception as error:
        #     return Response({'message': 'Some error Occured', "error": error})

    def send_order_confirmation_email(self, order, user):
        subject = 'Order Confirmation'
        message = f'Thank you for your order!\n\nOrder ID: {order.order_ref_id}\nTotal Amount Paid: {order.order_total}'
        from_email = 'foodie@example.com'
        to_email = [user.email]

        send_mail(subject, message, from_email, to_email, fail_silently=False)

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
    lookup_field = 'order_ref_id'
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order_data = serializer.validated_data
        product_items = order_data.get('product_items', [])

        if request.user.is_superuser:
            try:
                if "delivery_agent" in request.data:
                    agent_slug = request.data['delivery_agent']
                    agent_instance = DeliveryAgent.objects.get(user__username=agent_slug)
                    instance.delivery_agent = agent_instance
                    instance.order_status = "assigned"
                    instance.save()
            except Exception as error:
                pass
        elif DeliveryAgent.objects.filter(user=request.user).exists():
            try:
                if "order_status" in request.data:
                    status_slug = request.data['order_status']
                    if status_slug == "deliveried":
                        generated_otp = otp_generator()
                        self.send_order_confirmation_email(instance, request.user, generated_otp)
                    instance.otp = generated_otp
                    instance.save()
                    return Response({'order_id': instance.order_ref_id, 'message': 'Your order OTP has been sent to user Email successfully.',
                                      'User Email': instance.customer_name.user.email})
            except Exception as error:
                return Response({'message': 'Some error Occured'})
        elif Customer.objects.filter(user=request.user).exists(): 
            try:
                if "otp" in request.data:
                    otp = request.data['otp']
                    if otp == instance.otp:
                        instance.order_status = "deliveried"
                    instance.save()
                    self.send_order_confirmation_email(instance, request.user, is_delivery_successful=True)
                    return Response({'order_id': instance.order_ref_id, 'message': 'Your order has been Deliveried successfully.',
                                      'User Email': instance.customer_name.user.email})
                elif "order_status" in request.data:
                    status_slug = request.data['order_status']
                    if status_slug == "canceled":
                        # Check if the order can be canceled (within 30 minutes of creation)
                        time_difference = timezone.now() - instance.created_at
                        if time_difference.total_seconds() < 30 * 60 :
                            # Cancel the order
                            instance.order_status = "canceled"
                            instance.save()
                            return Response({'order_id': instance.order_ref_id, 'message': 'Your order has been canceled successfully.',
                                            'User Email': instance.customer_name.user.email})
                        else:
                            return Response({'message': 'Sorry, you can only cancel the order within 30 minutes of creation.'})
            except Exception as error:
                return Response({'message': 'Some error Occured'})

        OrderItem.objects.filter(order=instance).delete()
        if product_items:
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

    def send_order_confirmation_email(self, order, user, otp=None, is_delivery_successful=False):
        subject = 'Order Confirmation'
        if is_delivery_successful:
            message = f'Thank you for your order!\n\nOrder ID: {order.order_ref_id}\n Amount Paid: {order.order_total}\nYour order has been delivered!'
        else:
            message = f'Thank you for your order!\n\nOrder ID: {order.order_ref_id}\n Amount Paid: {order.order_total}'
        from_email = 'foodie@example.com'
        to_email = [user.email]
        send_mail(subject, message, from_email, to_email, fail_silently=False)
