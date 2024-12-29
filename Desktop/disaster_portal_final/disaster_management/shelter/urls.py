# shelter/urls.py
from django.urls import path
from .views import shelter_search, shelter_detail

urlpatterns = [
    path('search/', shelter_search, name='shelter_search'),
    path('shelter/<int:shelter_id>/', shelter_detail, name='shelter_detail'),
]
