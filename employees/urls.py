from django.urls import path
from employees.views import employee_hierarchy, load_subordinates, employee_list, user_login, user_logout

urlpatterns = [
  path('', employee_hierarchy, name='employee_hierarchy'),
  path('load_subordinates/<int:employee_id>/', load_subordinates, name='load_subordinates'),
  path('list/', employee_list, name='employee_list'),
  path('login/', user_login, name='login'),
  path('logout/', user_logout, name='logout'),
]
