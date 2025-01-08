from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, timedelta
import uuid
from django.conf import settings

def default_variable_id_expiry():
    """Returns the default expiry time for variable_id."""
    return now() + timedelta(hours=settings.VARIBLE_ID_REFRESH_INTERVAL_HOURS/3600)
def session_expiry_time():
    """Returns the  expiry time for session."""
    return now() + settings.ACCESS_TOKEN_LIFETIME

class ChatRoom(models.Model):
    """Model to represent a chat room."""
    name = models.CharField(max_length=255, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='chat_rooms')
    variable_id = models.UUIDField(default=uuid.uuid4, editable=False)
    variable_id_expiry = models.DateTimeField(default=default_variable_id_expiry, editable=False)

    def __str__(self):
        return self.name or f"Private Chat ({self.id})"

class ChatSession(models.Model):
    """Tracks user sessions in a chat room."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    session_expiry = models.DateTimeField(default=session_expiry_time, editable=False)

class Message(models.Model):
    """Model to store messages."""
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"

class todaysSpecial(models.Model):
    """Model to store todays special."""
    special = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Coupon(models.Model):
    """Model to store coupons."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    coupon_code = models.CharField(max_length=255)
