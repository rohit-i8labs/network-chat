from django.contrib import admin
from .models import ChatRoom,Message,ChatSession
# Register your models here.

admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(ChatSession)