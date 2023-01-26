from rest_framework import serializers
from .models import *
from custom_user.serializers import *

class AssetSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(
        read_only=True,
        slug_field = 'name'
    )
    company = CompanySerializer()
    current_holder = EmployeeSerializer()

    class Meta:
        model = Asset
        fields = "__all__"



class AssetLoanSessionSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    supervisor = EmployeeSerializer()
    asset = AssetSerializer()

    class Meta:
        model=AssetLoanSession
        fields = "__all__"