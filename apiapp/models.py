from django.db import models


# Create your models here.
class Message(models.Model):
    value = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
