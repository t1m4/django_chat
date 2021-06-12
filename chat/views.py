from asgiref.sync import sync_to_async
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.signals import request_finished
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.functional import cached_property
from django.views import View

from login.auth_views import AsyncView, AsyncLoginRequiredMixin


class IndexView(AsyncLoginRequiredMixin):
    template_name = 'chat/html/index.html'
    context = {}

    async def get(self, request, *args, **kwargs):
        self.context['users'] = await self.get_users(request)
        return await sync_to_async(render)(request, self.template_name, context=self.context)

    @sync_to_async
    def get_users(self, request, size: int = 10, *args, **kwargs):
        return User.objects.filter(is_active=True).exclude(id=request.user.id).order_by('-id')[0:size]


class UserChatView(AsyncLoginRequiredMixin):
    template_name = 'chat/html/chat.html'
    context = {}

    async def get(self, request, id, *args, **kwargs):
        self.context['id'] = id
        return await sync_to_async(render)(request, self.template_name, context=self.context)
