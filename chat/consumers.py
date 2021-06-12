import asyncio
import datetime
import json
from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


# from core.models import Game, Chat, ChatMessage
# from core.models import Chat, ChatMessage, Client
# from core.utils import get_object_or_none
from django.contrib.auth.models import User
from django.db.models import Q

from chat.models import Chat, ChatMessage
from login.tools import get_object_or_none


class TradingConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        if self.scope['user'].is_authenticated:
            await self.update_user(self.scope['user'])
            await self.send({
                "type": "websocket.accept"
            })
            while True:
                i = await self.all_online_users()
                await self.send({
                    'type': 'websocket.send',
                    'text': '{}'.format(i)
                })
                await asyncio.sleep(60)


    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def update_user(self, user):
        user.profile.last_online = datetime.datetime.now()
        user.save()
    @database_sync_to_async
    def all_online_users(self):
        return User.objects.filter(profile__last_online__gte=datetime.datetime.now()-datetime.timedelta(minutes=15)).count()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope['user'].is_authenticated:
            await self.update_user(self.scope['user'])
            self.username = await self.get_username(self.scope['user'])
            chat_id = self.scope['url_route']['kwargs'].get('id')
            user_two = await get_object_or_none(User, id=chat_id)
            self.chat, id = await self.get_or_create(self.scope['user'], user_two)
            self.room_group_name = 'chat_%i' % id
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        else:
            await self.disconnect(1001)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        await self.create_chat_message(user, message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    @database_sync_to_async
    def update_user(self, user):
        """
        Update user online time, every times when he connect to server using websocket
        """
        user.profile.last_online = datetime.datetime.now()
        user.save()

    @database_sync_to_async
    def get_or_create(self, u1, u2):
        """
        Create Chat using two users
        """
        chat = Chat.objects.filter(Q(user_one=u1) & Q(user_two=u2) | Q(user_one=u2) & Q(user_two=u1))
        if chat.count() == 0:
            chat = Chat.objects.create(user_one=u1, user_two=u2)
        else:
            chat = chat[0]
        return chat, chat.id

    @database_sync_to_async
    def create_chat_message(self, user, message):
        """
        Create Chat Message
        """
        return ChatMessage.objects.create(chat=self.chat, user=user, message=message)

    @database_sync_to_async
    def get_username(self, user):
        return user.username