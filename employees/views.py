from django.shortcuts import render
from django.db.models import Q

from employees.models import Employee


def employee_hierarchy(request):
  top_level_employees = Employee.objects.filter(manager__isnull=True)
  return render(request, 'employees/hierarchy.html', {'employees': top_level_employees})


def load_subordinates(request, employee_id):
  employee = Employee.objects.get(id=employee_id)
  subordinates = employee.subordinates.all()
  return render(request, 'employees/subordinates.html', {'subordinates': subordinates})


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
