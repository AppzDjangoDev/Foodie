from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import FoodProduct
from .serializers import FoodProductSerializer

@method_decorator(csrf_exempt, name='dispatch')
class FoodProductAPIView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, code=None):
        if code:
            food_product = get_object_or_404(FoodProduct, code=code)
            serializer = FoodProductSerializer(food_product)
        else:
            food_products = FoodProduct.objects.all()
            serializer = FoodProductSerializer(food_products, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        # Ensure that request.POST is converted to a dictionary
        data = dict(request.POST)
        print("datadatadata", data)
        # Now you can access values using data.get()
        name = data['name'][0]
        code = str(data['code'][0])
        price = data['price'][0]
        print("priceprice", code)
        # Convert 'price' to a float (adjust as needed based on your requirements)
        try:
            price = float(price)
        except ValueError:
            return JsonResponse({'error': 'Invalid price value'}, status=400)
        # Add other data validations as needed
        serializer = FoodProductSerializer(data={'name': name,'code': code,  'price': price })
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Food product added successfully','data': serializer.data}, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    def put(self, request, code):
        product = get_object_or_404(FoodProduct, code=code)
        # Use request.POST to access x-www-form-urlencoded data
        name = request.POST.get('name', '')
        price = request.POST.get('price', '')
        print("namename", name, "priceprice", price)
        try:
            # Update the FoodProduct instance
            if name:
                product.name = name
            if price:
                product.price = price
            product.save()

            # Optionally, use a serializer to respond with the updated data
            serializer = FoodProductSerializer(product)
            return JsonResponse(serializer.data)

        except Exception as error:
            print("error", error)
            return JsonResponse({'error': str(error)}, status=500)

    def delete(self, request, code):
        food_product = get_object_or_404(FoodProduct, code=code)
        food_product.delete()
        return JsonResponse({'message': 'Food product deleted successfully'}, status=204)
