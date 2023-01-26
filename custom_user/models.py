from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from uuid import uuid4
from django.core.validators import RegexValidator

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200, default="")
    contact_no = models.CharField(
        max_length=16,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{8,15}$",
                message="Contact number must be entered in the format '+123456789'. Up to 15 digits allowed.",
            ),
        ],)

    def __str__(self):
        return f"ID: {self.pk} | Name: {self.name} | Address: {self.address} | Contact No. {self.contact_no}"


class CustomUser(AbstractUser):
    # Groups
    GROUP_MANAGER = "MANAGER"
    GROUP_EMPLOYEE = "EMPLOYEE"

    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(
        max_length=16,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{8,15}$",
                message="Phone number must be entered in the format '+123456789'. Up to 15 digits allowed.",
            ),
        ],
    )
    name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]



class Employee(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.PROTECT,
        related_name="employee"
        )
    department = models.CharField(max_length=40)
    employee_id = models.CharField(
        max_length=80, help_text="Employee ID assigned by the company"
    )
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name="get_associated_company"
    )
    is_company_admin = models.BooleanField()
    in_service = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        
        if self.is_company_admin:
            group_name = self.user.GROUP_MANAGER
        else:
            group_name = self.user.GROUP_EMPLOYEE

        group = Group.objects.get_or_create(name=group_name)[0]
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} | ID: {self.pk}"

    class Meta:
        unique_together = ["employee_id", "company"]