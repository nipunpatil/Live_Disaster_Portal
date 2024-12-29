from django.urls import path
from .views import alert_map, alert_list
from .views import login_view, signup_view
urlpatterns = [
    path('', alert_map, name='alert_map'),     # URL for the map HTML
    
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),

    path('alerts/', alert_list, name='alert_list'),  # New URL for alerts
]
