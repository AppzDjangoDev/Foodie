# Generated by Django 3.2.19 on 2023-11-23 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_management', '__first__'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_ref_id', models.CharField(default=0, max_length=6, unique=True)),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('assigned', 'Assigned'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('delivered_at', models.DateTimeField(null=True)),
                ('payment_mode', models.CharField(max_length=20)),
                ('order_total', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('otp', models.CharField(max_length=20)),
                ('customer_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.customer')),
                ('delivery_agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.deliveryagent')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order_management.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_management.foodproduct')),
            ],
        ),
    ]