from django.shortcuts import render
from .models import EmergencyContact

def emergency_contacts(request):
    contacts = EmergencyContact.objects.all()
    return render(request, 'emergency/contacts.html', {'contacts': contacts})
