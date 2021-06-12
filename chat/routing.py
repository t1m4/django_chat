from django.urls import re_path, path

from chat import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.TradingConsumer.as_asgi()),
    path('ws/chat/<int:id>/', consumers.ChatConsumer.as_asgi()),
]