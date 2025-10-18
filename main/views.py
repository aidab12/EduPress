from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView

from .forms import LoginForm


