"""
URL configuration for staff_hierarchy project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/', include('employees.urls')),
]
