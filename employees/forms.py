from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
  manager_name = forms.CharField(required=False, label='Manager',
                                 widget=forms.TextInput(
                                   attrs={
                                     'class': 'form-control',
                                     'id': 'manager-autocomplete'
                                   })
                                 )

  class Meta:
    model = Employee
    fields = ['name', 'position', 'hire_date', 'email', 'manager_name']

  def __init__(self, *args, **kwargs):
    super(EmployeeForm, self).__init__(*args, **kwargs)
    if self.instance and self.instance.pk:
      self.fields['manager_name'].initial = self.instance.manager.name if self.instance.manager else ''

  def save(self, commit=True):
    instance = super(EmployeeForm, self).save(commit=False)
    manager_name = self.cleaned_data.get('manager_name')
    if manager_name:
      try:
        manager = Employee.objects.filter(name=manager_name).first()
        instance.manager = manager
      except Employee.DoesNotExist:
        instance.manager = None
    if commit:
      instance.save()
    return instance