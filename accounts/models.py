from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('platform_owner', 'Platform Owner'),
        ('restaurant_owner', 'Restaurant Owner'),
        ('customer', 'Customer'),
    ]

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
    )

    def __str__(self):
        return f"{self.username} ({self.user_type})"
