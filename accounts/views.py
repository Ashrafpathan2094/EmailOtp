from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request , 'home.html')

def login_attempt(request):
    return render(request , 'login.html')


def register_attempt(request):
    return render(request , 'register.html')


def success(request):
    return render(request , 'success.html')

def token_send(request):
    return render(request , 'token_send.html')

def verify(request , auth_token):
    return redirect('/')


def error_page(request):
    return  render(request , 'error.html')
