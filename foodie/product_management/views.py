import random
import string
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .models import FoodProduct
from .serializers import FoodProductSerializer

def generate_unique_code():
    while True:
        # Generate the remaining six characters (numbers)
        code_gen = ''.join(random.choices(string.ascii_uppercase, k=6))
        # Check if the product_code already exists in the FoodProduct table
        if not FoodProduct.objects.filter(product_code=code_gen).exists():
            return code_gen

class FoodProductListCreateView(generics.ListCreateAPIView):
    queryset = FoodProduct.objects.all()
    serializer_class = FoodProductSerializer

    def create(self, request, *args, **kwargs):
        # Add logic to generate a unique 6-digit code for the new product
        product_code = generate_unique_code()
        print("product_code", product_code)
        # Modify request.data directly to set the product code
        request.data['product_code'] = product_code
        return super().create(request, *args, **kwargs)


class FoodProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodProduct.objects.all()
    serializer_class = FoodProductSerializer
    lookup_field = 'product_code'
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Get the fields to update from the request data
        fields_to_update = request.data.keys()
        # Ensure that the fields to update are valid fields in the serializer
        valid_fields = set(FoodProductSerializer().get_fields().keys())
        invalid_fields = set(fields_to_update) - valid_fields
        if invalid_fields:
            return Response({"error": f"Invalid fields: {', '.join(invalid_fields)}"}, status=status.HTTP_400_BAD_REQUEST)
        # Perform partial updates for each field
        for field in fields_to_update:
            value = request.data.get(field)
            setattr(instance, field, value)
        # Save the updated instance
        instance.save()
        # Return the updated data
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)