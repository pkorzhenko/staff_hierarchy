from django.urls import path
from employees.views import (
  employee_hierarchy,
  load_subordinates,
  employee_list,
  user_login,
  user_logout,
  employee_create,
  employee_update,
  employee_delete,
  search_managers,
  change_manager
)

urlpatterns = [
  path('', employee_hierarchy, name='employee_hierarchy'),
  path('load_subordinates/<int:employee_id>/', load_subordinates, name='load_subordinates'),
  path('list/', employee_list, name='employee_list'),
  path('login/', user_login, name='login'),
  path('logout/', user_logout, name='logout'),
  path('create/', employee_create, name='employee_create'),
  path('update/<int:pk>/', employee_update, name='employee_update'),
  path('delete/<int:pk>/', employee_delete, name='employee_delete'),
  path('search_managers/', search_managers, name='search_managers'),
  path('change_manager/', change_manager, name='change_manager'),
]
