from custom_user.permissions import *
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework import response,status
from django.utils import timezone

class InStockAssetListAPIView(generics.ListAPIView):
    permission_classes = [IsCompanyAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = AssetSerializer
    
    def get_queryset(self):
        return Asset.objects.filter(company=self.request.user.employee.company, is_available=True)



class NotInStockAssetListAPIView(generics.ListAPIView):
    permission_classes = [IsCompanyAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = AssetSerializer
    
    def get_queryset(self):
        return Asset.objects.filter(company=self.request.user.employee.company, is_available=False)


class CompanyLoanSessionListAPIView(generics.ListAPIView):
    permission_classes = [IsCompanyAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = AssetLoanSessionSerializer
    
    def get_queryset(self):
        return AssetLoanSession.objects.filter(asset__company=self.request.user.employee.company)


class AssetLoanSessionListAPIView(generics.ListAPIView):
    permission_classes = [IsCompanyAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = AssetLoanSessionSerializer
    
    def get_queryset(self):
        pk = self.request.parser_context['kwargs']['pk']
        return AssetLoanSession.objects.filter(asset__company=self.request.user.employee.company, asset=pk)



class AssetCreateAPIView(generics.CreateAPIView):
    serializer_class = AssetSerializer
    permission_classes = [IsCompanyAdmin]
    authentication_classes = [TokenAuthentication]
    
    def perform_create(self, serializer):
        return serializer.save(
            company = self.request.user.employee.company
        )


class EmployeeLoanSessionListAPIView(generics.ListAPIView):
    permission_classes = [IsCompanyAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = AssetLoanSessionSerializer
    
    def get_queryset(self):
        pk = self.request.parser_context['kwargs']['pk']
        return AssetLoanSession.objects.filter(asset__company=self.request.user.employee.company, employee=pk)

class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    permission_classes = [IsCompanyAdmin]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

    def get_queryset(self):
        return Asset.objects.filter(company=self.request.user.employee.company)




class AssignAssetView(generics.CreateAPIView):
    permission_classes = [IsCompanyAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = AssetLoanSessionSerializer


    def isCompanyEmployee(self, company, employee_id):
        try:
            employee = Employee.objects.get(pk=employee_id)
            return employee.company == company and employee.in_service
        except Employee.DoesNotExist:
            return False

    def isCompanyAsset(self, company, asset_id):
        try:
            asset = Asset.objects.get(pk=asset_id)
            return asset.company == company
        except Asset.DoesNotExist:
            return False


    def create(self, request, *args, **kwargs):
        try:
            req_obj = self.request.data
            employee_id = req_obj['employee']
            asset_id = req_obj['asset']
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            if(self.isCompanyAsset(self.request.user.employee.company, asset_id) and self.isCompanyEmployee(self.request.user.employee.company, employee_id)):
                asset = Asset.objects.get(pk=asset_id)
                if(asset.is_available):
                    asset.current_holder = Employee.objects.get(pk=employee_id)
                    asset.is_available = False
                    asset.save()
                    serializer.save(
                        supervisor = self.request.user.employee
                    )
                    return response.Response(
                        serializer.data, status=status.HTTP_201_CREATED
                    )
                else:
                    return response.Response({'error': 'This asset has already been taken'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return response.Response({'error': 'You do not have permission for this action'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            print(e)
            return response.Response({'error': 'Server Error Occurred'}, status=status.HTTP_400_BAD_REQUEST)



class ReturnAssetView(generics.UpdateAPIView):
    permission_classes = [IsCompanyAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = AssetLoanSessionSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        asset_id = request.data['asset']
        asset = Asset.objects.get(pk=asset_id)
        if(asset.company == self.request.user.employee.company):
            asset.current_holder = None
            asset.is_available = True
            asset.save()

            serializer.save(
                returned_at = timezone.now()
            )
            return response.Response({'message': 'Asset recieved successfully'}, status=status.HTTP_200_OK)
        
        else:
            return response.Response({'message': 'You do not have permission for this action'}, status=status.HTTP_401_UNAUTHORIZED)