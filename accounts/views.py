from wsgiref import validate
from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .helpers import send_forget_password_mail, send_mail_after_registration
import re
from django.utils import timezone
from datetime import timedelta



EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


@login_required(login_url="/login")
def home(request):
    return render(request, 'home.html')




def login_attempt(request):

    #Get Data
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        incorrect_username_password_message = 'Wrong username or password.'


        #validating the data
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, incorrect_username_password_message)
            return redirect('/login')

        #Check if Account is Verified
        profile_obj = Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/login')
        #Authenticate the User
        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, incorrect_username_password_message)
            return redirect('/login')

        login(request, user)
        return redirect('/')
    return render(request, 'login.html')


def register_attempt(request):
    #Get Data
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')

        try:
            #Data Validation
            if (not username):
                messages.success(request, 'Username Required')
                return redirect('/register')
            elif len(username) <= 4 :
                messages.success(request,"Username too short.")
                return redirect("/register")
            elif len(username) > 14:
                messages.success(request,"Username too Long.")
                return redirect("/register")
            
            if (not email):
                messages.success(request, 'Email Required')
                return redirect('/register')
            elif email and not re.match(EMAIL_REGEX,email):
                messages.success(request, 'Enter Valid Email')
                return redirect('/register')

            if password != repeat_password:
                messages.success(request, 'Both Password Should Match')
                return redirect('/register')
            if len(password) <= 6:
                messages.success(request,"Password too Short")
                return redirect("/register")
            

            if User.objects.filter(username=username).first():
                messages.success(request, 'Username Already Taken')
                return redirect('/register')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email Already Taken')
                return redirect('/register')
            #if data is valid create user
            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            #create profile object
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            #send mail to verify
            send_mail_after_registration(email, auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, 'register.html')


def verify(request, auth_token):

    try:
        
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            #check if already verified
            if profile_obj.is_verified:
                messages.success(request, 'Your account has already been verified')
                return redirect('/login')
            #verifies account
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified')
            return redirect('/login')
        else:
            return redirect('/error')

    except Exception as e:
        print(e)


def error_page(request):
    return render(request, 'error.html')


def success(request):
    return render(request, 'success.html')


def token_send(request):
    return render(request, 'token_send.html')


def change_password(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')


            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
            if len(new_password) <= 6:
                messages.success(request,"Password too Short")
                return redirect(f'/change-password/{token}/')

            


            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            profile_obj.forget_password_token = ""
            messages.success(request, 'Password Changed.')
            return redirect('/login/')

    except Exception as e:
        print(e)
    return render(request, 'change-password.html', context)


def forget_password(request):
    try:
        #get data
        if request.method == 'POST':
            username = request.POST.get('username')
            #validate data
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')
            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An Email is sent to your email id.')
            return redirect('/forget-password/')

    except Exception as e:
        print(e)

    return render(request, 'forget-password.html')
