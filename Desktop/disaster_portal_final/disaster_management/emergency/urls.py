from django.urls import path
from . import views

urlpatterns = [
    path('contacts/', views.emergency_contacts, name='emergency_contacts'),
]
