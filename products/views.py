from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .serializers import ProductSerializer
from .models import Product
from rest_framework.response import Response
from rest_framework import exceptions, status, generics, mixins
from users.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from testdrive.pagination import CustomPageNumberPagination

class ProductGenericApiView(
    generics.GenericAPIView, 
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination
    
    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data            
            })

        return self.list(request)
        
    def post(self, request):
        return Response({
            'message': 'User created successfully',
            'data': self.create(request).data
        }, status=status.HTTP_201_CREATED)
        
    def put(self, request, pk=None):
        return Response({
            'message': 'User updated',
            'data': self.partial_update(request, pk).data
        })
    
    def delete(self, request, pk=None):
        self.destroy(request, pk)
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class FileUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # parser_classes = ['multipart/form-data']
    parser_classes = (MultiPartParser, )
    
    def post(self, request):
        file = request.FILES.get('image')
        # file_name = default_storage.save(file.name, ContentFile(file.read()))
        file_name = default_storage.save(file.name, file)
        url = default_storage.url(file_name)
        # if not file:
        #     raise exceptions.ValidationError({'file': 'File is required'})
        
        return Response({
            'url': 'http://localhost:8000/api' + url
        }, status=status.HTTP_201_CREATED)  
 