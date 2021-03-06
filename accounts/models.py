from hashlib import md5
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    auth_token = models.CharField(max_length=100)
    forget_password_token = models.CharField(max_length=100, blank=True)
    datetime = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.username
