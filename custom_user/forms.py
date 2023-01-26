from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Employee


class CreateUserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'name', 'password']



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"