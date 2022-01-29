from django.urls import path,include
from django.urls import path
from .views import *

urlpatterns = [
    path('', home ,name = "home"),
]