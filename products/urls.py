from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import ProductGenericApiView, FileUploadView
urlpatterns = [
    path('products', ProductGenericApiView.as_view()),
    path('products/<str:pk>', ProductGenericApiView.as_view()),
    path('upload', FileUploadView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)