from django.core.management.base import BaseCommand
from employees.models import Employee
from faker import Faker


class Command(BaseCommand):
  help = 'Seed the database with employee data'

  def handle(self, *args, **kwargs):
    fake = Faker()
    managers = []

    # Create top-level managers
    for _ in range(10):
      name = fake.name()
      hire_date = fake.date_this_decade()
      email = fake.email()
      try:
        manager = Employee.objects.create(
          name=name,
          position='Manager',
          hire_date=hire_date,
          email=email
        )
        managers.append(manager)
      except:
        print(f"manager exists: {email} {name} {hire_date}")

    # Create employees under each manager
    for manager in managers:
      for _ in range(5000):
        name = fake.name()
        hire_date = fake.date_this_decade()
        email = fake.email()
        try:
          Employee.objects.create(
            name=name,
            position='Employee',
            hire_date=hire_date,
            email=email,
            manager=manager
          )
        except:
          print(f"employee exists: {email} {name} {hire_date}")

    self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
