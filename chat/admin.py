from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from chat.models import User, Chat, Profile, ChatMessage


class ChatAdmin(admin.ModelAdmin):
    list_display = ('user_one', 'user_two')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_online',)


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user', 'message')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
