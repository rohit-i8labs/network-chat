from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

class ChatRoomListCreateView(generics.ListCreateAPIView):
    """View to list and create chat rooms."""
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        chat_room = serializer.save()
        chat_room.members.add(self.request.user)


class MessageListCreateView(generics.ListCreateAPIView):
    """View to list and send messages in a chat room."""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_room_id = self.kwargs['chat_room_id']
        return Message.objects.filter(chat_room_id=chat_room_id)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
