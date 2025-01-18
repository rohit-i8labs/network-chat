# accounts/models.py
from datetime import time
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('restaurant_owner', 'Restaurant Owner'),
        ('customer', 'Customer'),
    ]

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='customer',  # Default value set to 'customer'
    )
    user_token_expiry = models.TimeField(default=time(0, 0))  # Default to 00:00 (midnight)
    current_var_id = models.CharField(max_length=10, null=True, blank=True)
    current_restaurant = models.ForeignKey(
        'chat.Restaurant', on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.user_type})"
