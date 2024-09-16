from django.db import models

class Product(models.Model):
    # TODO: Add an image field to the Product model
    # // The image field is a file field that allows the user to upload an image
    # // upload_to='products/' is the directory where the image will be stored
    # // null=True, blank=True allows the image to be optional
    # image = models.ImageField(upload_to='products/', null=True, blank=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
