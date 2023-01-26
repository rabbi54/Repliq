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
# Create your views here.




class CompanyAssetListView(ListView, LoginRequiredMixin, IsCompanyAdmin):
    model = Asset
    template_name = 'asset/dashboard.html'
    context_object_name = "assets"
    def get_queryset(self):
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



class AssetUpdateView(UpdateView, LoginRequiredMixin, IsCompanyAdmin):
    form_class=AssetForm
    template = 'asset/asset_form.html'
    model = Asset
    success_url = reverse_lazy('dashboard')


class AssignAssetView(CreateView, LoginRequiredMixin, IsCompanyAdmin):
    form_class = LoanSessionForm
    model = AssetLoanSession
    success_url = reverse_lazy('dashboard')


    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.supervisor=self.request.user.employee
        self.object.expires_at = timezone.now() + timedelta(days=30)

        self.object.asset.is_available = False
        self.object.asset.current_holder = form.cleaned_data['employee']

        self.object.asset.save()
        self.object.save()
        return super().form_valid(form)



class LoanListView(ListView, LoginRequiredMixin, IsCompanyAdmin):
    model = AssetLoanSession
    template_name = 'asset/loan_list.html'
    context_object_name = "loans"
    
    def get_queryset(self):

        print(settings.STATIC_URL)
        print(settings.STATIC_ROOT)
        queryset = AssetLoanSession.objects.filter(
            asset__company = self.request.user.employee.company
        )
        return queryset
    


class ReturnAsset(APIView, LoginRequiredMixin, IsCompanyAdmin):
    def post(self, request, format=None):
        try:
            loan_id = request.data.get("id").strip()
            try:
                loan = AssetLoanSession.objects.get(pk=loan_id)
                loan.returned_at = timezone.now()

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
