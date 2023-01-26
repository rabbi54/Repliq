from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('user-register/', register, name='user-register'),
    path('user-login', auth_views.LoginView.as_view(
        template_name='user/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'),
         name='user-logout'),
    path("add-employee/", AddEmployee.as_view(), name='add-employee'),
]
