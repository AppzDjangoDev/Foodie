# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import DeliveryAgent, Customer
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
import uuid
import random
import string

@user_passes_test(lambda u: u.is_superuser)
def add_delivery_agent(request):
    if request.method == 'POST':
        try:
            # Handle form submission to create a new delivery agent
            # Send email with username and auto-generated password
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = User.objects.make_random_password()
            username = generate_unique_username()
            phone_number=request.POST['phone_number']
            print("entry1", email)
            user = User.objects.create_user(username, email, password)
            DeliveryAgent.objects.create(user=user)
            delivery_agent_user = DeliveryAgent.objects.get(user=user.id)
            # Update the Userdetails
            delivery_agent_user.user.first_name = first_name
            delivery_agent_user.user.last_name = last_name
            delivery_agent_user.user.phone_number = phone_number
            delivery_agent_user.user.save()
            print("entry2")
            try:
                send_mail('Welcome to the system', f'Your username: {username}\nYour password: {password}', 'from@example.com', [email])
            except Exception as e :
                print("entry3", e)
            return JsonResponse({'message': 'Delivery agent added successfully!'})
        except Exception as  e :
            print("error", e)
            return JsonResponse({'message': 'Delivery agent registartion failed!'})

@user_passes_test(lambda u: u.is_superuser)
def add_customer(request):
    if request.method == 'POST':
        try:
            # Handle form submission to create a new delivery agent
            # Send email with username and auto-generated password
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = User.objects.make_random_password()
            username = generate_unique_username()
            phone_number=request.POST['phone_number']
            print("entry1", email)
            user = User.objects.create_user(username, email, password)
            Customer.objects.create(user=user)
            customer_user = Customer.objects.get(user=user.id)
            # Update the Userdetails
            customer_user.user.first_name = first_name
            customer_user.user.last_name = last_name
            customer_user.user.phone_number = phone_number
            customer_user.user.save()
            print("entry2")
            try:
                send_mail('Welcome to the system', f'Your username: {username}\nYour password: {password}', 'from@example.com', [email])
            except Exception as e :
                print("entry3", e)
            return JsonResponse({'message': 'Delivery agent added successfully!'})
        except Exception as  e :
            print("error", e)
            return JsonResponse({'message': 'Delivery agent registartion failed!'})
        
def generate_unique_username():
    # Generate a unique username using uuid and random characters
    unique_id = str(uuid.uuid4().hex)[:6]  # Using the first 6 characters of the UUID
    random_chars = ''.join(random.choice(string.ascii_letters) for _ in range(2))
    username = f'{random_chars.upper()}{unique_id[:2]}'
    return username[:8] 

@user_passes_test(lambda u: u.is_superuser)
def update_delivery_agent(request, agent_username):
    agent = get_object_or_404(DeliveryAgent, user__username=agent_username)
    if request.method == 'POST':
        # Handle form submission to update delivery agent information
        try :
            if request.POST.get('phone_number'):
                agent.user.phone_number = request.POST.get('phone_number')
            if request.POST.get('email'):
                agent.user.email = request.POST.get('email')
            if request.POST.get('is_blocked'):
                agent.user.is_blocked = request.POST.get('is_blocked')
            if request.POST.get('first_name'):
                agent.user.first_name = request.POST.get('first_name')
            if request.POST.get('last_name'):
                agent.user.last_name = request.POST.get('last_name')
            agent.user.save()
        except Exception as e:
            print("error", e)
            return JsonResponse({'message': 'Delivery agent update failed! Some Error Occured '})
        return JsonResponse({'message': 'Delivery agent updated successfully!'})
    else:
        return JsonResponse({'message': 'Delivery agent update failed! Check request method.'})

@user_passes_test(lambda u: u.is_superuser)
def update_customer(request, customer_username):
    customer = get_object_or_404(Customer, user__username=customer_username)
    if request.method == 'POST':
        # Handle form submission to update delivery customer information
        try :
            if request.POST.get('phone_number'):
                customer.user.phone_number = request.POST.get('phone_number')
            if request.POST.get('email'):
                customer.user.email = request.POST.get('email')
            if request.POST.get('is_blocked'):
                customer.user.is_blocked = request.POST.get('is_blocked')
            if request.POST.get('first_name'):
                customer.user.first_name = request.POST.get('first_name')
            if request.POST.get('last_name'):
                customer.user.last_name = request.POST.get('last_name')
            customer.user.save()
        except Exception as e:
            print("error", e)
            return JsonResponse({'message': 'Customer update failed! Some Error Occured '})
        return JsonResponse({'message': 'Customer updated successfully!'})
    else:
        return JsonResponse({'message': 'Customer update failed! Check request method.'})

@user_passes_test(lambda u: u.is_superuser)
def delivery_agent_list(request):
    agents = DeliveryAgent.objects.all()
    agent_list = [{'id': agent.user.id, 'phone_number': agent.user.phone_number, 'blocked': agent.user.is_blocked, 'email': agent.user.email} for agent in agents]
    return JsonResponse({'agents': agent_list})

@user_passes_test(lambda u: u.is_superuser)
def customer_list(request):
    customers = Customer.objects.all()
    customer_list = [{'id': customer.id, 'name': customer.name, 'email': customer.email} for customer in customers]
    return JsonResponse({'customers': customer_list})
