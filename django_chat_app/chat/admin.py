from dataclasses import field, fields
from re import search
from django.contrib import admin

from .models import Chat, Message

class MessageAdmin(admin.ModelAdmin):
    fields = ('chat', 'text', 'created_at', 'author', 'receiver')
    list_display = ('created_at', 'text', 'author', 'receiver')
    search_fields = ('text',)

class ChatAdmin(admin.ModelAdmin):
    fields = ('created_at', 'creator', 'chatter')
    list_display = ('created_at', 'creator', 'chatter')
    search_fields = ('creator', 'chatter',)

# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat, ChatAdmin)
