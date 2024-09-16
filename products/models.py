from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
