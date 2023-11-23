# serializers.py
from rest_framework import serializers
from .models import FoodProduct

class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProduct
        fields = '__all__'
