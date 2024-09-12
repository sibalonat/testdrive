from django.urls import path
from .views import index, register, login, AuthenticatedUser, logout

urlpatterns = [
    path('users', index),
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('user', AuthenticatedUser.as_view()),
]