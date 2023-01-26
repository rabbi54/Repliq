from .views import *
from django.urls import path

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register')
]
