from django.contrib import admin
from .models import Asset, Brand, AssetLoanSession
# Register your models here.
admin.site.register(Asset)
admin.site.register(Brand)
admin.site.register(AssetLoanSession)