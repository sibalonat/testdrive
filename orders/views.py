import csv
from django.http import HttpResponse
from django.shortcuts import render

from .serializers import OrderSerializer
from .models import Order
from rest_framework import generics, mixins
from rest_framework.views import APIView
from testdrive.pagination import CustomPageNumberPagination
from users.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.
class OrderGenericApiView(
    generics.GenericAPIView, 
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPageNumberPagination
    
    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data            
            })

        return self.list(request)
    
class ExportApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        
        orders = Order.objects.all()
        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Email', 'Product Title', 'Price', 'Quantity'])
        
        for order in orders:
            writer.writerow([order.id, order.name, order.email, '', '', ''])
            order_items = order.order_items.all()
            # order_items = OrderItem.objects.all().filter(order_id=order.id)
            for order_item in order_items:
                writer.writerow(['', '', '', order_item.product_title, order_item.price, order_item.quantity])
        
        return response