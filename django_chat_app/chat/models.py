from django.db import models
from datetime import date
from django.contrib.auth.models import User


# Create your models here.

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
