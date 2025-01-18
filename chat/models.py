import random
import string
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta
from icecream import ic
from django.utils.timezone import now

def generate_unique_var_id():
    """Generate a unique 6-digit alphanumeric ID."""
    return ''.join(random.choices(string.digits, k=6))


class Restaurant(models.Model):
    QR_GEN_FREQUENCY_CHOICES = [
        ('hourly', 1),
        ('daily', 24),
        ('weekly', 168),
        ('monthly', 730),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='media/images', null=True, blank=True)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_restaurant")
    total_customers = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    avg_stay_time = models.DurationField(default=timedelta(minutes=0))
    todays_special = models.TextField()
    customers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="visited_restaurants", blank=True)
    total_messages = models.IntegerField(default=0)
    var_id = models.CharField(max_length=6, unique=True, null=True,blank=True, default=generate_unique_var_id)
    qr_gen_frequency = models.CharField(max_length=20, choices=QR_GEN_FREQUENCY_CHOICES)
    var_id_gen_time = models.DateTimeField(default=now)
    var_id_expiry_time = models.DateTimeField(null=True,blank=True)
    total_qr_scanned = models.IntegerField(default=0)
    token_refresh_frequency = models.PositiveIntegerField(default=1, help_text="Time in hours")

    def save(self, *args, **kwargs):
        # Ensure var_id is unique before saving
        if not self.var_id:
            self.var_id = self.generate_unique_var_id()
        # Calculate var_id_expiry_time
        qr_hours = dict(self.QR_GEN_FREQUENCY_CHOICES)[self.qr_gen_frequency]
        print("==========================")
        # ic(qr_hours)
        # ic(self.var_id_gen_time)
        # ic(timedelta(hours=qr_hours))
        self.var_id_expiry_time = self.var_id_gen_time + timedelta(hours=qr_hours)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_var_id():
        """Generate a unique var_id if default fails."""
        while True:
            var_id = generate_unique_var_id()
            if not Restaurant.objects.filter(var_id=var_id).exists():
                return var_id

    def __str__(self):
        return self.name

class Offer(models.Model):
    description = models.TextField()
    time_based = models.BooleanField(default=False)
    duration = models.PositiveIntegerField(default=1, help_text="Duration in hours if time-based")

    def __str__(self):
        return f"Offer: {self.description[:50]}{'...' if len(self.description) > 50 else ''}"

class Message(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    is_private = models.BooleanField(default=False)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages", null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"