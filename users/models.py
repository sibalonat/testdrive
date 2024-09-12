from django.db import models
from django.contrib.auth.models import AbstractUser

class Permission(models.Model):
    name = models.CharField(max_length=200)
class Role(models.Model):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission)

class User(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
