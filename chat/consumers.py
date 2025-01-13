import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message,ChatSession
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
import asyncio
from datetime import datetime, timedelta, timezone
import uuid
from icecream import ic
from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']  #Get Permanent Room id
        self.room_group_name = f"chat_{self.room_id}"

        # Parse query string to extract parameters
        query_params = parse_qs(self.scope['query_string'].decode())

        # Extract specific parameters
        self.variable_id = query_params.get('variable_id', [None])[0]  #Var Room id passed by user
        token = query_params.get('token', [None])[0]   # Token of User

        # Authenticate user via token
        self.user = await self.get_user_from_token(token)
        ic("Details passed by user")
        ic(self.room_id,self.variable_id, token)

        # Validate the variable_id
        chat_room = await self.get_chat_room(self.room_id)#Fetch current var room ID by permanent id
        ic(chat_room.variable_id)
        
        if chat_room.variable_id != uuid.UUID(self.variable_id):
            await self.accept()
            await self.send(text_data=json.dumps({
                "error": "invalid room id",
            }))
            await self.close()
            return

        # Check and manage session
        self.session = await self.get_or_create_session(self.user, chat_room)#Create or get user dession details

        # Make current time offset-aware
        current_time = datetime.now(timezone.utc)
        ic(current_time,self.session.session_expiry,self.session.joined_at)
        if current_time > self.session.session_expiry:
            ic("----------here-------------")
            await self.accept()
            await self.send(text_data=json.dumps({
                "error": "session expired please re conect",
            }))
            await self.close()  
            return
        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'session_expiry'):
            self.session_expiry.cancel()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        current_time = datetime.now(timezone.utc)
        ic(current_time,self.session.session_expiry,self.session.joined_at)
        if current_time > self.session.session_expiry:
            ic("----------here-------------")
            await self.send(text_data=json.dumps({
                "error": "session expired please re conect",
            }))
            await self.close()  
            return
        
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
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_or_create_session(self, user, chat_room):
        session, created = ChatSession.objects.get_or_create(user=user, chat_room=chat_room)
        return session

    @sync_to_async
    def get_chat_room(self, room_id):
        try:
            return ChatRoom.objects.get(id=room_id) or ChatRoom.objects.get(permanent_id=room_id)
        except ChatRoom.DoesNotExist:
            return None

    @sync_to_async
    def get_user_from_token(self, token):
        try:
            access_token = AccessToken(token)  # Validate the token
            user_id = access_token['user_id']  # Extract the user ID from the token
            return User.objects.get(id=user_id)
        except Exception:
            return None
