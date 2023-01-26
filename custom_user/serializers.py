from rest_framework import serializers
from .models import *



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    company = CompanySerializer()
    
    class Meta:
        model = Employee
        fields = [
            'user',
            'department',
            'employee_id',
            'company',
        ]
        read_only_fields = [
            'is_company_admin',
        ]