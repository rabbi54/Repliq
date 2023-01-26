from django.urls import path, include
from asset.api_views import CompanyLoanSessionListAPIView
from .models import *
from .api_views import *
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('assets', AssetViewSet, basename='company')

api_urls = [
    path('asset_in_stock/', InStockAssetListAPIView.as_view()),
    path('asset_not_in_stock/', NotInStockAssetListAPIView.as_view()),

    path('company-asset-loan-list/', CompanyLoanSessionListAPIView.as_view()),

    path('asset-loan-list/<int:pk>/', AssetLoanSessionListAPIView.as_view()),

    path('create-asset/', AssetCreateAPIView.as_view()),
    path('employee-loan-list/<int:pk>/', EmployeeLoanSessionListAPIView.as_view()),
    
    path('assign-asset/', AssignAssetView.as_view()),

    path('return-asset/', ReturnAssetView.as_view())


]



urlpatterns = [
    path('api/', include(api_urls)),
    path('', CompanyAssetListView.as_view(), name="dashboard"),
    path('asset-update/<int:pk>/',AssetUpdateView.as_view(), name="asset-update"),
    path("assign-asset/", AssignAssetView.as_view(), name='assign-asset'),
    path('show-loans/',LoanListView.as_view(), name="show_loans"),
    path('loan-returned/',ReturnAsset.as_view(), name="loan_returned")
]

urlpatterns+=router.urls