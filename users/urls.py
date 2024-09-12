from django.urls import path
from .views import index, register, login, AuthenticatedUser

urlpatterns = [
    path('users', index),
    path('register', register),
    path('login', login),
    path('user', AuthenticatedUser.as_view()),
]