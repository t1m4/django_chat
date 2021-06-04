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

from login.auth_views import AsyncView, MyLoginRequiredMixin


class IndexView(MyLoginRequiredMixin):
    template_name = 'chat/html/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.context)
