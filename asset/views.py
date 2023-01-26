from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, UpdateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from asset.forms import *
from custom_user.permissions import IsCompanyAdmin
from .models import *
from django.contrib import messages
from django.utils import timezone
from django.urls.base import reverse_lazy
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
