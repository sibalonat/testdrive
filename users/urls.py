from django.urls import path
from .views import index, register, login

urlpatterns = [
    path('users', index),
    path('register', register),
    path('login', login),
]