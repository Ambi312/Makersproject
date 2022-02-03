from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='users')

    def __str__(self):
        return self.get_full_name()