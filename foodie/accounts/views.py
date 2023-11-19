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
            print("entry1")
            # Check if the email is unique
            if User.objects.filter(email=email).exists():
                # Handle the case where the email is not unique (you can raise an exception, redirect, or return an error response)
                print("Error: Email already exists")
                # Handle the error (e.g., return a response to the user)
                return HttpResponse("Error: Email already exists")
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
        
def generate_unique_username():
    # Generate a unique username using uuid and random characters
    unique_id = str(uuid.uuid4().hex)[:6]  # Using the first 6 characters of the UUID
    random_chars = ''.join(random.choice(string.ascii_letters) for _ in range(2))
    username = f'{random_chars.upper()}{unique_id[:2]}'
    return username[:8] 

@user_passes_test(lambda u: u.is_superuser)
def update_delivery_agent(request, agent_id):
    agent = get_object_or_404(DeliveryAgent, id=agent_id)
    if request.method == 'POST':
        # Handle form submission to update delivery agent information
        agent.phone_number = request.POST['phone_number']
        agent.blocked = 'block' in request.POST
        agent.save()
        return JsonResponse({'message': 'Delivery agent updated successfully!'})
    else:
        return JsonResponse({'message': 'Delivery agent update failed!'})

@user_passes_test(lambda u: u.is_superuser)
def delivery_agent_list(request):
    agents = DeliveryAgent.objects.all()
    agent_list = [{'id': agent.id, 'phone_number': agent.phone_number, 'blocked': agent.blocked} for agent in agents]
    return JsonResponse({'agents': agent_list})

@user_passes_test(lambda u: u.is_superuser)
def customer_list(request):
    customers = Customer.objects.all()
    customer_list = [{'id': customer.id, 'name': customer.name, 'email': customer.email} for customer in customers]
    return JsonResponse({'customers': customer_list})
