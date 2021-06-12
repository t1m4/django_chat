from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_online = models.DateTimeField(null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Chat(models.Model):
    user_one = models.ForeignKey(User, on_delete=models.PROTECT, related_name='chat_one', )
    user_two = models.ForeignKey(User, on_delete=models.PROTECT, related_name='chat_two', )

    def __str__(self):
        return "{}-{}".format(self.user_one, self.user_two)


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    message = models.CharField(max_length=255)
