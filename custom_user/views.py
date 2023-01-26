from django.shortcuts import render, redirect
from rest_framework.generics import GenericAPIView
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework import response, status
from rest_framework.authtoken.models import Token

from .forms import *
# Create your views here.



class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)


        if serializer.is_valid():
            serializer.save(username=serializer.data['email'])
            user = CustomUser.objects.get(email=serializer.data['email'])
            token, is_cr = Token.objects.get_or_create(user=user)

            return response.Response({'payload':serializer.data, 
            'token' : str(token)}, status = status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status = status.HTTP_400_BAD_REQUEST)



def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            # group = Group.objects.get(name='Customers')
            # user.groups.add(group)
            return redirect('user-login')
    else:
        form = CreateUserForm()
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)