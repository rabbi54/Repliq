from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class AssetPartialForm(forms.ModelForm):
    """
        Partial Form to create an asset
    """
    class Meta:
        model = Asset
        fields = [
            'brand',
            'company',
            'model',
            'name',
            'serial_no',
            'inventory_no',
            'identifier'
        ]


class AssetForm(forms.ModelForm):

    """
        To update an asset requiered form
    """
    class Meta:
        model = Asset
        exclude = [
            'is_avaiable',
            'current_holder'
        ]


class LoanSessionForm(forms.ModelForm):

    # filter out other company employees and assets
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        print(kwargs)
        super().__init__(*args, **kwargs)

        self.fields['employee'].queryset=Employee.objects.filter(company=user.employee.company)

        self.fields['asset'].queryset=Asset.objects.filter(company=user.employee.company, is_available=True)
        

    class Meta:
        model = AssetLoanSession
        fields = [
            "employee",
            "asset",
            "remarks",
            "note",
            "contract",
        ]
