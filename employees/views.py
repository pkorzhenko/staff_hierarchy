from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from employees.models import Employee


def employee_hierarchy(request):
  top_level_employees = Employee.objects.filter(manager__isnull=True)
  return render(request, 'employees/hierarchy.html', {'employees': top_level_employees})


def load_subordinates(request, employee_id):
  employee = Employee.objects.get(id=employee_id)
  subordinates = employee.subordinates.all()
  return render(request, 'employees/subordinates.html', {'subordinates': subordinates})

def user_login(request):
      if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(request, username=username, password=password)
          if user is not None:
              login(request, user)
              return redirect('employee_list')
          else:
              return render(request, 'employees/login.html', {'error': 'Invalid credentials'})
      return render(request, 'employees/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def employee_list(request):
  query = request.GET.get('q')
  sort_by = request.GET.get('sort_by', 'name')
  employees = Employee.objects.all()

  if query:
    employees = employees.filter(
      Q(name__icontains=query) |
      Q(position__icontains=query) |
      Q(email__icontains=query)
    )

  employees = employees.order_by(sort_by)
  return render(request, 'employees/employee_list.html', {'employees': employees})
