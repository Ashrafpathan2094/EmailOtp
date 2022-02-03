from lib2to3.pgen2 import token
import profile
from urllib.request import Request
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
from .helpers import send_forget_password_mail,send_mail_after_registration

@login_required(login_url="/")
def home(request):
    return render(request , 'home.html')

def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/accounts/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/accounts/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/accounts/login')
        
        login(request , user)
        return redirect('/')

    return render(request,'login.html')


def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:

            if User.objects.filter(username=username).first():
                messages.success(request,'Username Already Taken')
                return redirect('/register')

            if User.objects.filter(email=email).first():
                messages.success(request,'Email Already Taken')
                return redirect('/register')

            user_obj = User.objects.create(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())

            profile_obj = Profile.objects.create(user = user_obj,auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('/token') 

        except Exception as e :
            print(e)


    return render(request , 'register.html')




def verify(request , auth_token):

    try:

        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:

            if profile_obj.is_verified:
                 messages.success(request,'Your account has already been verified')
                 return redirect('/login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Your account has been verified')
            return redirect('/login')
        else:
            return redirect('/error')

    except Exception as e :
        print(e)

def error_page(request):
    return  render(request , 'error.html')

def success(request):
    return render(request , 'success.html')

def token_send(request):
    return render(request , 'token_send.html')

def ChangePassword(request):
    context = {}

    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id': profile_obj.user_id}
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            reconfirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request,"User not Found")
                return redirect(f'/change-password/{token}/')
            if new_password != reconfirm_password:
                messages.success(request,"Both password should be same")
                return redirect(f'/change-password/{token}/')



        user_obj = User.objects.get(id = user_id)
        user_obj.set_password(new_password)
        user_obj.save()
        return redirect("/login/")

    except Exception as e:
        print(e)

    return render(request , 'change-password.html')



def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email,token)
            messages.success(request, 'An Email is sent to your email id.')
            return redirect('/forget-password/')

            
    
    except Exception as e:
        print(e)

    return render(request , 'forget-password.html')




