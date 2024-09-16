from django.shortcuts import render

from .serializers import ProductSerializer
from .models import Product
from rest_framework.response import Response
from rest_framework import exceptions, status, generics, mixins
from users.authentication import JWTAuthentication
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
 