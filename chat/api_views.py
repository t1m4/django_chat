from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response

from chat.serializers import UserSerializer
from login.auth_views import AsyncView, AsyncLoginRequiredMixin


class UserView(AsyncLoginRequiredMixin):
    result = {'status': 'ok', 'users': []}
    async def get(self, request, *args, **kwargs):
        try:
            size = int(request.GET.get('size'))
        except:
            size = 10
        size = 10 if size > 10 else size
        users = await self.get_users(size, request)
        serializer = UserSerializer(users, many=True)
        data = await self.get_serializer_data(serializer)
        self.result['users'] = data
        return JsonResponse(self.result)

    @sync_to_async
    def get_users(self, size, request, *args, **kwargs):
        return User.objects.filter(is_active=True).exclude(id=request.user.id).order_by('-id')[0:size]
    @sync_to_async
    def get_serializer_data(self, serializer, *args, **kwargs):
        return serializer.data
