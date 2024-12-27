from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import ChatRoom, Message, ChatSession
from .serializers import ChatRoomSerializer, MessageSerializer, ChatSessionSerializer

class ChatRoomViewSet(viewsets.ModelViewSet):
    """ViewSet to list and create chat rooms."""
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        chat_room = serializer.save()
        chat_room.members.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet to list and send messages in a chat room."""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_room_id = self.kwargs['chat_room_id']
        return Message.objects.filter(chat_room_id=chat_room_id)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class ChatSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet to fetch ChatSession data for the authenticated user."""
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        # Fetch ChatSession instances related to the authenticated user
        user_sessions = self.get_queryset()
        serializer = self.get_serializer(user_sessions, many=True)
        return Response(serializer.data)
