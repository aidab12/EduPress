from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView

from .forms import LoginForm


class SendCodeAPIView(APIView):
    pass


class LoginAPIView(APIView):
    pass


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                # добавляем возврат для случая user == None
                return HttpResponse('Invalid username or password')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})
