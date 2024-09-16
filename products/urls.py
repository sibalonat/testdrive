from django.urls import path

from .views import ProductGenericApiView
urlpatterns = [
    path('products', ProductGenericApiView.as_view()),
    path('products/<str:pk>', ProductGenericApiView.as_view()),
]