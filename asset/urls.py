from django.urls import path, include
from .api_views import InStockAssetListAPIView


api_urls = [
    path('asset_in_stock/', InStockAssetListAPIView.as_view()),
]

urlpatterns = [
    path('api/', include(api_urls))
]
