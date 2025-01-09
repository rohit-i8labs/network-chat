from rest_framework import serializers
from .models import ChatRoom, Message,ChatSession, todaysSpecial, Coupon
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','first_name','last_name']

class ChatRoomSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'is_group', 'members',"variable_id","variable_id_expiry"]

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'sender', 'text', 'timestamp']

class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['id', 'chat_room', 'user', 'joined_at',"session_expiry"]

class TodaysSpecialserializer(serializers.ModelSerializer):
    class Meta:
        model =  todaysSpecial
        fields = ['special','timestamp']        

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Coupon
        fields = ['name','description','coupon_code']                