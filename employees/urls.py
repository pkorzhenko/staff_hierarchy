from django.urls import path
from .views import employee_hierarchy, load_subordinates

urlpatterns = [
  path('', employee_hierarchy, name='employee_hierarchy'),
  path('load_subordinates/<int:employee_id>/', load_subordinates, name='load_subordinates'),
]
