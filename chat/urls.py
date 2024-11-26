from django.urls import path
from .views import ChatRoomListCreateView, MessageListCreateView


urlpatterns = [
    path('chatrooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('chatrooms/<int:chat_room_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
]
