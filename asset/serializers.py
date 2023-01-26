from rest_framework import serializers
from .models import *
from custom_user.serializers import *

class AssetSerializer(serializers.ModelSerializer):
    # show only brand name
    brand = serializers.SlugRelatedField(
        read_only=True,
        slug_field = 'name'
    )
    # company serializer provides add the fildes
    company = CompanySerializer()
    current_holder = EmployeeSerializer()

    class Meta:
        model = Asset
        fields = "__all__"

        read_only_fields = [
            'company',
            "current_holder",
        ]



class AssetLoanSessionSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    supervisor = EmployeeSerializer()
    asset = AssetSerializer()

    class Meta:
        model=AssetLoanSession
        fields = "__all__"