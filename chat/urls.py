from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, MessageViewSet, ChatSessionViewSet

# Initialize the router
router = DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet, basename='chatroom')
router.register(r'chatrooms/(?P<chat_room_id>\d+)/messages', MessageViewSet, basename='message')
router.register(r'chat_sessions', ChatSessionViewSet, basename='chat_session')

# URLs for the app
urlpatterns = [
    path('', include(router.urls)),  # Include the router-generated URLs
]
