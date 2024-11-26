import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"

        # Authenticate user via token
        try:
            token = self.scope['query_string'].decode().split('token=')[-1]
            self.user = await self.get_user_from_token(token)
            if not self.user:
                raise AuthenticationFailed("Invalid token")
        except Exception as e:
            await self.close()  # Close the WebSocket connection if authentication fails
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Fetch chat room using async method
        chat_room = await self.get_chat_room(self.room_id)

        # Save message to database using sync_to_async
        msg = await sync_to_async(Message.objects.create)(
            chat_room=chat_room, sender=self.user, text=message
        )

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'timestamp': str(msg.timestamp),
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_chat_room(self, room_id):
        return ChatRoom.objects.get(id=room_id)

    @sync_to_async
    def get_user_from_token(self, token):
        try:
            access_token = AccessToken(token)  # Validate the token
            user_id = access_token['user_id']  # Extract the user ID from the token
            return User.objects.get(id=user_id)
        except Exception:
            return None
