from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Admin(AbstractUser):
    pass


class User(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    chat_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)
