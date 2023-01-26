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
        self.object.save()
        return super().form_valid(form)