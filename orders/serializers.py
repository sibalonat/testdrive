from .models import OrderItem, Order
from rest_framework import serializers

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField('get_total')
    def get_total(self, obj):
        items = OrderItem.objects.all().filter(order_id=obj.id)
        return sum([item.price * item.quantity for item in items])
    
    class Meta:
        model = Order
        fields = '__all__'
        
    # def create(self, validated_data):
    #     order_items = validated_data.pop('order_items')
    #     order = Order.objects.create(**validated_data)
        
    #     for order_item in order_items:
    #         OrderItem.objects.create(order=order, **order_item)
            
    #     return order