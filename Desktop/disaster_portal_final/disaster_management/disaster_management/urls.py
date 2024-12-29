from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alerts/', include('alerts.urls')),
    path('shelter/', include('shelter.urls')),
    path('emergency/', include('emergency.urls')),
    path('', include('alerts.urls')),  # For home or general pages
]
