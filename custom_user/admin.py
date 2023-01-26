from django.contrib import admin
from .models import CustomUser, Company, Employee
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(Employee)