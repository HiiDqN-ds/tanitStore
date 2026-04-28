from django.shortcuts import render
from tickets.models import Ticket
from django.contrib import messages

def index(request):
    """View for the home page"""
    return render(request, 'home/index.html')

def create_ticket(request):
    """Public page for creating repair tickets"""
    context = {}
    
    if request.method == 'POST':
        # Retrieve and save form data
        new_ticket = Ticket.objects.create(
            client_first_name=request.POST.get('client_first_name'),
            client_last_name=request.POST.get('client_last_name'),
            client_email=request.POST.get('client_email'),
            client_phone=request.POST.get('client_phone'),
            device_type=request.POST.get('device_type'),
            device_model=request.POST.get('device_model'),
            problem_description=request.POST.get('problem_description'),
            tracking_id=request.POST.get('tracking_id') or None
        )
        
        # Pass the new ticket instance to the template
        context['ticket'] = new_ticket
        messages.success(request, "Ticket created successfully!")

    return render(request, 'home/create_ticket.html', context)
