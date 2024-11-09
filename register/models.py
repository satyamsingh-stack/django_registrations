from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class People(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=255,unique=True)
    password=models.CharField(max_length=255)