from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=200, min_length=6, write_only=True
    )
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password',
            'phone',
        ]

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email = validated_data['email'],
            phone = validated_data['phone'],
            name = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

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