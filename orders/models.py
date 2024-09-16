from django.db import models

# Create your models here.
class Order(models.Model):
    # order_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def name(self):
        return self.first_name + ' ' + self.last_name
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

class OrderItem(models.Model):
    # product_id = models.IntegerField()
    product_title = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    # total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'order_items'
        ordering = ['-created_at']
