from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework import response, status
from rest_framework.authtoken.models import Token
# Create your views here.



class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)


        if serializer.is_valid():
            serializer.save()
            user = CustomUser.objects.get(email=serializer.data['email'])
            token, is_cr = Token.objects.get_or_create(user=user)

            return response.Response({'payload':serializer.data, 
            'token' : str(token)}, status = status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status = status.HTTP_400_BAD_REQUEST)