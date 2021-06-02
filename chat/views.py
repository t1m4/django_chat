from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from login.auth_views import AsyncView


class IndexView(AsyncView):
    async def get(self, request, *args, **kwargs):
        return HttpResponse('ok', status=200)