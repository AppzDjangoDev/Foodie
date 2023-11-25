from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=12, null=False)
    is_blocked = models.BooleanField(default=False)
    email = models.EmailField(blank=True, unique=True, null=False)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class DeliveryAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Create or get the 'Delivery Agents' group and add the user to it
        delivery_agents_group, created = Group.objects.get_or_create(name='Delivery Agents')
        self.user.groups.add(delivery_agents_group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Create or get the 'Customers' group and add the user to it
        customers_group, created = Group.objects.get_or_create(name='Customers')
        self.user.groups.add(customers_group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


