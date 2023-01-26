from django.db import models
from custom_user.models import Company, CustomUser, Employee



# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=50, help_text="Brand")
    description = models.TextField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at',]

    def get_assets(self):
        return self.asset_set.filter(brand=self)

    def __str__(self) -> str:
        return f"{self.name}"


class Asset(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        related_name="get_brand_assets",
        help_text="Brand of the asset",
        null=True
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="get_company_assets"
    )

    model = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    serial_no = models.CharField(max_length=40,null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    inventory_no = models.CharField(max_length=40, null=True, blank=True)
    identifier = models.CharField(max_length=40,
        null=True, blank=True, help_text="External identifier.")
    invoice = models.FileField(null=True, blank=True)
    warranty = models.FileField(null=True, blank=True)
    purchased_at = models.DateTimeField(null=True)

    current_holder = models.ForeignKey(
        Employee, on_delete=models.PROTECT, null=True, blank=True, related_name="get_associated_assets"
    )

    is_available = models.BooleanField(default=True)
    


    def get_active_sessions(self):
        return self.assetloansession_set.filter(
            started_at__isnull=False,
            returned_at__isnull=True)
        
    def get_ended_sessions(self):
        return self.assetloansession_set.filter(
            started_at__isnull=False,
            returned_at__isnull=False)
    
    def get_latest_session(self):
        return self.assetloansession_set.latest("started_at")

    
    def __str__(self) -> str:
        return f"{self.name} | {self.brand} | {self.company.name}"


class AssetLoanSession(models.Model):


    def getSentinelUser():
        return CustomUser.objects.get_or_create(
        email="user@support.com",
        username="user@support.com",
        name="user",
        )[0]


    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET(getSentinelUser),
        related_name="get_asset_loans_taken"
    )

    supervisor = models.ForeignKey(Employee,
        related_name="get_asset_loans_supervised",
        on_delete=models.SET(getSentinelUser),
        null=True,
        )
    asset = models.ForeignKey(Asset,
        on_delete=models.CASCADE,
        related_name="get_associated_loans"
    )
    
    remarks = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    contract = models.FileField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at',]