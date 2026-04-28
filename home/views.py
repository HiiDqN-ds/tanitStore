from django.shortcuts import render, redirect
from tickets.models import Ticket
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

def index(request):
    return render(request, 'home/index.html')

def create_ticket(request):
    """Public page for creating repair tickets via AJAX"""
    context = {
        'tickets_url': '/tickets/',  # AJAX endpoint
    }
    return render(request, 'home/create_ticket.html', context)