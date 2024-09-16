from django.urls import path
from .views import ExportApiView, OrderGenericApiView

urlpatterns = [
    path('orders', OrderGenericApiView.as_view()),
    path('orders/<str:pk>', OrderGenericApiView.as_view()),
    path('export', ExportApiView.as_view()),
]