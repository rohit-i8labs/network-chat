from django.contrib import admin
from .models import ChatRoom,Message,ChatSession,todaysSpecial,Coupon
# Register your models here.

admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(ChatSession)
admin.site.register(todaysSpecial)
admin.site.register(Coupon)