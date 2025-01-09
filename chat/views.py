from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import ChatRoom, Message, ChatSession, todaysSpecial, Coupon
from django.contrib.auth.models import User
from .serializers import ChatRoomSerializer, MessageSerializer, ChatSessionSerializer,UserSerializer, TodaysSpecialserializer, CouponSerializer

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

class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer

    def create(self, request):
        """Handles user registration via POST."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password')
            if not password:
                return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=password
            )
            return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        permission_classes = [permissions.IsAuthenticated]
        """Allows authenticated users to view their details via GET."""
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
    
class TodaysSpecialViewSet(viewsets.ViewSet):
    queryset = todaysSpecial.objects.all().order_by('-timestamp')

    def list(self, request):
        """Fetch the list of today's specials."""
        queryset = self.queryset
        serializer = TodaysSpecialserializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Create a new today's special. Only by Admin"""
        if not request.user.is_authenticated:
            return Response({"error": "Authentication is required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_superuser and not request.user.is_staff:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        serializer = TodaysSpecialserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CouponViewSet(viewsets.ViewSet):
    queryset = Coupon.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """Fetch the list of today's specials."""
        queryset = self.queryset
        serializer = CouponSerializer(queryset, many=True)
        return Response(serializer.data)    