from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=5)
    city = models.CharField(max_length=25)
    image = models.ImageField(upload_to='users')

    def __str__(self):
        return self.username

