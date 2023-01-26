from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class AssetPartialForm(forms.ModelForm):

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
    class Meta:
        model = Asset
        exclude = [
            'is_avaiable',
            'current_holder'
        ]

