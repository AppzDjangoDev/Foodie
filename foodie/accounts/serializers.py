from accounts.models import User, DeliveryAgent, Customer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']

class DeliveryAgentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nest UserSerializer to include all fields

    class Meta:
        model = DeliveryAgent
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'required': False,
            },
            'user__username': {
                'required': False,
            },
            'user__phone_number': {
                'required': False,
            },
            # Add other fields you want to make not required
        }


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nest UserSerializer to include all fields

    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'required': False,
            },
            'user__username': {
                'required': False,
            },
            'user__phone_number': {
                'required': False,
            },
            # Add other fields you want to make not required
        }
