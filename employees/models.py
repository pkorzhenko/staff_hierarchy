from django.db import models


class Employee(models.Model):
  name = models.CharField(max_length=100)
  position = models.CharField(max_length=100)
  hire_date = models.DateField()
  email = models.EmailField(unique=True)
  manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')

  def __str__(self):
    return f"{self.name} {self.position}"

  class Meta:
    indexes = [
      models.Index(fields=['name']),
      models.Index(fields=['position']),
      models.Index(fields=['email']),
      models.Index(fields=['hire_date']),
      models.Index(fields=['manager'])
    ]
    verbose_name = "Employee"
    verbose_name_plural = "Employees"
