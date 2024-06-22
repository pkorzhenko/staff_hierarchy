from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator

from employees.models import Employee
from employees.forms import EmployeeForm


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
  order = request.GET.get('order', 'asc')
  employees = Employee.objects.all()

  if query:
    employees = employees.filter(
      Q(name__icontains=query) |
      Q(position__icontains=query) |
      Q(email__icontains=query)
    )

  if order == 'desc':
    sort_by = '-' + sort_by

  employees = employees.order_by(sort_by)
  paginator = Paginator(employees, 20)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    return JsonResponse({
      'employees': list(page_obj.object_list.values('id', 'name', 'position', 'hire_date', 'email')),
      'has_next': page_obj.has_next()
    })

  return render(request, 'employees/employee_list.html',
                {
                  'page_obj': page_obj,
                  'sort_by': sort_by,
                  'order': order,
                  'q': query
                 }
                )


@login_required
def employee_create(request):
  if request.method == 'POST':
    form = EmployeeForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('employee_list')
  else:
    form = EmployeeForm()
  return render(request, 'employees/employee_form.html', {'form': form})


@login_required
def employee_update(request, pk):
  employee = get_object_or_404(Employee, pk=pk)
  if request.method == 'POST':
    form = EmployeeForm(request.POST, instance=employee)
    if form.is_valid():
      form.save()
      return redirect('employee_list')
  else:
    form = EmployeeForm(instance=employee)
  return render(request, 'employees/employee_form.html', {'form': form})


@login_required
def employee_delete(request, pk):
  employee = get_object_or_404(Employee, pk=pk)
  if request.method == 'POST':
    employee.delete()
    return redirect('employee_list')
  return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})


def search_managers(request):
  if 'term' in request.GET:
    qs = Employee.objects.filter(name__icontains=request.GET.get('term'))
    names = list()
    for employee in qs:
      names.append(employee.name)
    return JsonResponse(names, safe=False)
  return JsonResponse([], safe=False)
