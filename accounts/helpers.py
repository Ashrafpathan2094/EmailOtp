from email import message
from django.conf import settings
from django.core.mail import send_mail
from .views import *
from .models import *



def send_mail_after_registration(email,token):
    subject = "Your Account needs to be verified"
    message = f"Hii Use this link to verify your account http://127.0.0.1:8000/verify/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def send_forget_password_mail(email,token):
    subject = "Your Forget Password link is"
    message = f"Hii Use this link to reset your password http://127.0.0.1:8000/change-password/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

    