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


class TradingConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.i = 0
        if self.scope['user'].is_authenticated:
            await self.update_user(self.scope['user'])
            await self.send({
                "type": "websocket.accept"
            })
            while True:
                await asyncio.sleep(1)
                self.i = await self.all_online_users()
                await self.send({
                    'type': 'websocket.send',
                    'text': '{}'.format(self.i)
                })


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
            print(self.scope['user'])

        #     get_string = self.scope['query_string'].decode('utf-8')
        #     get_string = get_string.split('&')
        #     get_string_id = get_string[0].split('=')
        #     if get_string_id[0] == 'id':
        #         self.admin = True
        #         self.user = await self.get_client(int(get_string_id[1]))
        #         self.room_group_name = 'chat_%s' % self.user.get_login()
        #         self.chat = await self.create_chat(self.user)
        #         # await self.print(self.user, self.room_group_name, self.chat)
        #
        #         # Join room group
        #         await self.channel_layer.group_add(
        #             self.room_group_name,
        #             self.channel_name
        #         )
        #     await self.accept()
        # else:
        #     self.user = await self.get_client(self.scope['session']['client_id'])
        #     print(self.user)
        #     self.room_group_name = 'chat_%s' % self.user.get_login()
        #     self.chat = await self.create_chat(self.user)
        #     # await self.print(self.chat)
        #     # Join room group
        #     await self.channel_layer.group_add(
        #         self.room_group_name,
        #         self.channel_name
        #     )
        #     await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print(close_code)
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if self.admin:
            user_login = self.scope['user'].username
        else:
            user_login = self.user.login
        await self.create_chat_message(self.chat, message, user_login)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': user_login + ': ' + message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def update_user(self, user):
        user.profile.last_online = datetime.datetime.now()
        user.save()
