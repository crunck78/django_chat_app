from datetime import date, datetime
from email.policy import default
from typing import Any
from xml.parsers.expat import model
from django.db import models
from datetime import date
from django.conf import settings

# from django.dispatch import receiver
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.


class ChatManager(models.Manager):
    def get_queryset(self):
        created = super().get_queryset().filter(creator=settings.AUTH_USER_MODEL)
        chatter = super().get_queryset().filter(chatter=settings.AUTH_USER_MODEL)
        return created + chatter


class Chat(models.Model):
    created_at = models.DateField(default=date.today)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        related_name='creator'
    )

    chatter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        related_name='chatter'
    )

    objects = models.Manager()
    current_objects = ChatManager()


class MessageManager(models.Manager):
    def get_queryset(self):
        created = super().get_queryset().filter(author=settings.AUTH_USER_MODEL)
        receiver = super().get_queryset().filter(receiver=settings.AUTH_USER_MODEL)
        return created + receiver


class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateField(default=date.today)
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='chat_message_set',
        default=None,
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        related_name='author_message_set'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        related_name='receiver_message_set'
    )
    objects = models.Manager()  # The default manager.
    current_objects = MessageManager()  # The Dahl-specific manager.
