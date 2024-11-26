from django.contrib.auth.models import User
from django.db import models

class ChatRoom(models.Model):
    """Model to represent a chat room, either group or private."""
    name = models.CharField(max_length=255, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='chat_rooms')

    def __str__(self):
        return self.name or f"Private Chat ({self.id})"


class Message(models.Model):
    """Model to store messages."""
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"
