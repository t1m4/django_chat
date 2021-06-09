from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from chat.models import User, Chat, Profile
class ChatAdmin(admin.ModelAdmin):
    list_display = ('creator', 'friend')

    def creator(self, obj):
        return obj.users.first()
    def friend(self, obj):
        return obj.users.last()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_online', )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Chat, ChatAdmin)