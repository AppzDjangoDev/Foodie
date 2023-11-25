from django.shortcuts import render
from django.db import models

class FoodProduct(models.Model):
    product_name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()  # Add a text field for the product description
    product_image = models.ImageField(upload_to='products/')  # Add an image field for the product image
    product_charge = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name

