from django.urls import path
from .views import (
    PermissionAPIView, register, login, logout, AuthenticatedUser, RoleViewSet, UserGenericApiView
)
urlpatterns = [
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('user', AuthenticatedUser.as_view()),
    # path('user/<int:id>', AuthenticatedUser.as_view()),
    path('permissions', PermissionAPIView.as_view()),
    path('roles', RoleViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('roles/<str:pk>', RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
    path('users', UserGenericApiView.as_view()),
    path('users/<str:pk>', UserGenericApiView.as_view()),
]