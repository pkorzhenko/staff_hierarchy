from django.shortcuts import render

from employees.models import Employee


def employee_hierarchy(request):
  top_level_employees = Employee.objects.filter(manager__isnull=True)
  return render(request, 'employees/hierarchy.html', {'employees': top_level_employees})


def load_subordinates(request, employee_id):
  employee = Employee.objects.get(id=employee_id)
  subordinates = employee.subordinates.all()
  return render(request, 'employees/subordinates.html', {'subordinates': subordinates})
