# Create your views here.
from accounts.models import User
from django.core.mail import send_mail
from accounts.serializers import CustomerSerializer, DeliveryAgentSerializer, UserSerializer
from .models import DeliveryAgent, Customer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializers import DeliveryAgentSerializer, UserSerializer  # Import your UserSerializer
from django.contrib.auth.mixins import UserPassesTestMixin
from dj_rest_auth.views import LoginView as DjRestAuthLoginView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions

User = get_user_model()

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class CustomLoginView(DjRestAuthLoginView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            # Include any other user-related data you want in the response
        })
        
class DeliveryAgentListView( generics.ListCreateAPIView):
    queryset = DeliveryAgent.objects.all()
    serializer_class = DeliveryAgentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_data = self.request.data.get('user')
        password = User.objects.make_random_password()
        user_data['password'] = password

        user_serializer = UserSerializer(data=user_data)  # Corrected from 'serializer = 0(data=user_data)'
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.set_password(password)
        user.save()
        send_mail(
            'Account Created',
            f'Username: {user.username}\nPassword: {password}',
            'foodie@example.com',
            [user.email],
            fail_silently=False,
        )
        delivery_agent = serializer.save(user=user)  # Assuming 'user' is a field in DeliveryAgent model
        return Response(DeliveryAgentSerializer(delivery_agent).data, status=status.HTTP_201_CREATED)
    
class DeliveryAgentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = DeliveryAgent.objects.all()
    serializer_class = DeliveryAgentSerializer
    lookup_field = 'user__username'  # Set the lookup field to 'user__username'
    permission_classes = [IsAuthenticated] 

    def get_object(self):
        # Use the username from the URL to get the DeliveryAgent instance
        username = self.kwargs['user__username']
        return self.queryset.get(user__username=username)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_data = request.data.pop('user', {})  # Remove 'user' from data and get the user_data

        # Update the user-related fields if user_data is provided
        if user_data:
            user_instance = instance.user
            user_serializer = UserSerializer(user_instance, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"Username": user_instance.username ,"message": "Delivery Agent Details Updated Successfully"})

    def perform_destroy(self, instance):
        # Override perform_destroy to handle deletion
        user = instance.user
        instance.delete()
        # Return a response indicating successful deletion
        return Response(f'Delivery agent for {user.username} deleted successfully.', status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        # Support PUT requests for full updates using the same logic as PATCH
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = DeliveryAgentSerializer(queryset, many=True)
        return Response(serializer.data)


class CustomerListView( generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        user_data = self.request.data.get('user')
        password = User.objects.make_random_password()
        user_data['password'] = password
        user_serializer = UserSerializer(data=user_data)  # Corrected from 'serializer = 0(data=user_data)'
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.set_password(password)
        user.save()

        send_mail(
            'Account Created',
            f'Username: {user.username}\nPassword: {password}',
            'foodie@example.com',
            [user.email],
            fail_silently=False,
        )

        customer = serializer.save(user=user)  # Assuming 'user' is a field in Customer model
        return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)

class CustomerDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'user__username'  # Set the lookup field to 'user__username'

    def get_object(self):
        # Use the username from the URL to get the Customer instance
        username = self.kwargs['user__username']
        return self.queryset.get(user__username=username)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_data = request.data.pop('user', {})  
        # Update the user-related fields if user_data is provided
        if user_data:
            user_instance = instance.user
            user_serializer = UserSerializer(user_instance, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"Username": user_instance.username ,"message": "Customer Details Updated Successfully"})

    def perform_destroy(self, instance):
        # Override perform_destroy to handle deletion
        user = instance.user
        instance.delete()
        # Return a response indicating successful deletion
        return Response(f'Customer for {user.username} deleted successfully.', status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        # Support PUT requests for full updates using the same logic as PATCH
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)
