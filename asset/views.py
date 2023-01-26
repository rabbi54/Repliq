from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, UpdateView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from asset.forms import *
from custom_user.permissions import IsCompanyAdmin
from .models import *
from django.contrib import messages
from django.utils import timezone
from django.urls.base import reverse_lazy
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework import status, response
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

# Create your views here.




class CompanyAssetListView(LoginRequiredMixin, IsCompanyAdmin, ListView):
    """
        Provides a form to create an asset and shows all the asset of the company
        If user is not logged in redirect to log in page
    
    """
    model = Asset
    template_name = 'asset/dashboard.html'
    context_object_name = "assets"

    def get_queryset(self):
        queryset = Asset.objects.none()
        if self.request.user.is_authenticated:
            queryset = Asset.objects.filter(
                company = self.request.user.employee.company
            )
        return queryset
    

    def post(self, request):
        f = AssetPartialForm(request.POST, request.FILES)
        if f.is_valid():
            asset = f.save()
            asset.purchased_at = timezone.now()
            asset.save()
            messages.info(request, "New Asset Added successfully!")
        else:
            print(f.errors)
        return redirect('dashboard')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form']=AssetPartialForm()
        return context



class AssetUpdateView(LoginRequiredMixin, IsCompanyAdmin, UpdateView):
    # to update an asset
    form_class=AssetForm
    template = 'asset/asset_form.html'
    model = Asset
    success_url = reverse_lazy('dashboard')


class AssignAssetView( LoginRequiredMixin, IsCompanyAdmin,CreateView):
    form_class = LoanSessionForm
    model = AssetLoanSession
    success_url = reverse_lazy('dashboard')


    def get_form_kwargs(self):
        """Provides user info to filter out compnay related info."""
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        # supervisor is the current company admin
        self.object.supervisor=self.request.user.employee
        # loan will expire after 30 days
        self.object.expires_at = timezone.now() + timedelta(days=30)


        # as the asset is now holding a user it is not available
        self.object.asset.is_available = False
        self.object.asset.current_holder = form.cleaned_data['employee']

        self.object.asset.save()
        self.object.save()
        return super().form_valid(form)



class LoanListView(LoginRequiredMixin, IsCompanyAdmin,ListView):
    model = AssetLoanSession
    template_name = 'asset/loan_list.html'
    context_object_name = "loans"
    
    def get_queryset(self):
        queryset = AssetLoanSession.objects.filter(
            asset__company = self.request.user.employee.company
        )
        return queryset
    


class ReturnAsset(LoginRequiredMixin, IsCompanyAdmin,APIView):
    def post(self, request, format=None):
        try:
            loan_id = request.data.get("id").strip()
            try:
                loan = AssetLoanSession.objects.get(pk=loan_id)
                # user returend the asset
                loan.returned_at = timezone.now()
                # so the asset is now available
                loan.asset.is_available = True
                loan.asset.current_holder = None
                loan.asset.save()
                loan.save()
                return response.Response(
                    status=status.HTTP_200_OK, data={"success": "Returned successfully"}
                )
            except AssetLoanSession.DoesNotExist:
                return response.Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"error": "Loan not found"},
                )
        except KeyError:
            return response.Response(
                status=status.HTTP_400_BAD_REQUEST, data={"error": "Argument not found"}
            )
