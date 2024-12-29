from django.shortcuts import render
from .models import Alert
import folium

# def alert_map(request):
#     alerts = Alert.objects.all()
#     folium_map = folium.Map(location=[24.800001, 87.963262], zoom_start=12)

#     for alert in alerts:
#         lat, lng = map(float, alert.polygon.split()[0].split(','))
#         folium.Marker(
#             [lat, lng],
#             popup=f"{alert.headline}: {alert.description}",
#             tooltip=alert.area
#         ).add_to(folium_map)

#     map_html = folium_map._repr_html_()
#     return render(request, 'alerts/map.html', {'map': map_html})

def alert_list(request):
     alerts = Alert.objects.all()  # Retrieve all alerts
     return render(request, 'alerts/alerts.html', {'alerts': alerts})
from django.shortcuts import render
from .models import Alert  # Ensure to import your Alert model

def alerts_view(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', '')

    # Start with all alerts
    alerts = Alert.objects.all()

    # Filter alerts based on search query
    if search_query:
        alerts = alerts.filter(headline__icontains=search_query)  # Search by headline

    # Sort alerts based on selected criteria
    if sort_by == 'sent_time':
        alerts = alerts.order_by('sent_time')  # Adjust field name as needed
    elif sort_by == 'severity':
        alerts = alerts.order_by('severity')  # Ensure you have a severity field

    # Pass the alerts to the template
    return render(request, 'alerts.html', {'alerts': alerts, 'request': request})

from django.shortcuts import render
from .models import Alert
import json

import json
from django.http import JsonResponse
from .models import Alert  # Adjust this import based on your project structure
# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Alert  # Import your Alert model
# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Alert  # Import your Alert model
import json

def alert_map(request):
    # Fetch alert data from the database
    alerts = Alert.objects.all().values('event', 'polygon', 'headline', 'onset', 'expires', 'area_desc')
    alert_list = []

    for alert in alerts:
        # Example of extracting a coordinate from the polygon data
        coords = alert['polygon'].split(' ')
        if coords:
            latitude, longitude = map(float, coords[0].split(','))
            alert_list.append({
                'event': alert['event'],
                'location': {
                    'latitude': latitude,
                    'longitude': longitude
                },
                'headline': alert['headline'],
                'onset': alert['onset'].isoformat(),  # Convert datetime to ISO format for JSON
                'expires': alert['expires'].isoformat(),  # Convert datetime to ISO format for JSON
                'area_desc': alert['area_desc'],
            })

    # Convert alert_list to JSON string to pass to the template
    alert_data_json = json.dumps(alert_list)

    # Render the HTML page for the map with alert data
    return render(request, 'alerts/map.html', {'alert_data': alert_data_json})
# views.py
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomLoginForm, CustomSignupForm

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('home')  # Redirect to your desired page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Signup successful.')
            return redirect('home')  # Redirect to your desired page
    else:
        form = CustomSignupForm()

    return render(request, 'signup.html', {'form': form})
