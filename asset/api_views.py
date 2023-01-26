from custom_user.permissions import *
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .serializers import *
from .models import *


class InStockAssetListAPIView(generics.ListAPIView):
    permission_classes = [IsCompanyAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = AssetSerializer
    
    def get_queryset(self):
        return Asset.objects.filter(company=self.request.user.employee.company, is_available=True)