import json

from django.core import serializers
from django.contrib.auth.models import User
from django.db.models import Q

from chat.models import Chat, Message

from django.contrib.auth import authenticate


def get_searched_users(request_search):
    # MultiValueDictKeyError
    # https://stackoverflow.com/questions/5895588/django-multivaluedictkeyerror-error-how-do-i-deal-with-it
    # Better use Django Forms

    # https://stackoverflow.com/questions/23139657/django-get-all-users
    # 'QuerySet' object has no attribute '_meta'
    # https://stackoverflow.com/questions/45856557/queryset-object-has-no-attribute-meta

    # search for users were no chat created was
    # do not send passwords with users list
    searched = User.objects.filter(username__startswith=request_search)

    # https://stackoverflow.com/questions/22490379/how-to-return-an-array-of-objects-in-a-django-model/22490689
    return serializers.serialize('json', searched)


def get_conversation(user_id, request_user):
    selected_user = get_user_by_id(user_id)
    query_chat = get_query_chat(selected_user, request_user)

    hasChat = Chat.objects.filter(
        query_chat['selected_creator'] & query_chat['user_chatter'] |
        query_chat['selected_chatter'] & query_chat['user_creator']
    )
    # does a chat exist between selected user and logged in user?
    if (hasChat.count() > 0):
        return hasChat
    else:
        newChat = create_conversation(selected_user, request_user)
        return newChat


def validate_chatroom(chat_id, request_user):
    selected_chat = Chat.objects.get(id=chat_id)

    validate_membership(request_user, selected_chat)
    creator = selected_chat.creator
    chatter = selected_chat.chatter
    selected_messages = Message.objects.filter(chat=selected_chat)
    messages = selected_messages.order_by('created_at')
    selected_chat = serializers.serialize('json', [selected_chat])
    chats = get_requester_chats(request_user)
    context = {
        'chats': chats,
        'selected_chat': json.loads(selected_chat)[0],
        'messages': messages,
        'chatter': chatter,
        'creator': creator
    }
    return context


def validate_delete_message(message_id, request_user):
    message = Message.objects.get(id=message_id)
    validate_membership(request_user, message.chat)
    message.delete()


def validate_new_message(request_post):

    my_chat = get_chat_by_id(request_post.get('selected_chat', None))
    validate_membership(request_post.user, my_chat)
    new_message = Message.objects.create(
        text=request_post.get['textmessage'],
        chat=my_chat,
        author=request_post.user,  # ? can it not be
        receiver=my_chat.chatter
    )
    return new_message


def validate_membership(request_user, chat):
    creator = chat.creator
    chatter = chat.chatter
    if creator != request_user and chatter != request_user:
        raise CustomException(
            'This Chat does not exist or your are not a member of it!'
        )


def get_user_by_id(user_id):
    return User.objects.filter(pk=user_id)[0]


def get_chat_by_id(chat_id):
    return Chat.objects.get(id=chat_id)


def get_query_chat(selected_user, request_user):
    return {
        "selected_creator": Q(creator__username=selected_user.username),
        "selected_chatter": Q(chatter__username=selected_user.username),
        "user_creator": Q(creator__username=request_user.username),
        "user_chatter": Q(chatter__username=request_user.username),
    }


def create_conversation(selected_user, request_user):
    return Chat.objects.create(
        creator=request_user,
        chatter=selected_user,
    )


def get_requester_chats(request_user):
    objects_chat = Chat.objects
    creator = objects_chat.filter(creator__username=request_user.username)
    chatter = objects_chat.filter(chatter__username=request_user.username)
    chats = creator | chatter
    return chats


def validate_registration(request_post):
    password_match = (
        request_post.get('password') ==
        request_post.get('check_password')
    )
    user_exists = get_user_by_name(request_post.get('username'))

    if not password_match:
        raise CustomException('Password does not Match!')
    if user_exists:
        raise CustomException('This user already exists!')


def register_new_user(request_post):
    new_user = User.objects.create_user(
        username=request_post.get('username'),
        # email=request_post.get('email'),
        password=request_post.get('password')
    )
    return new_user


def validate_login(request_post):
    user = authenticate(
        username=request_post.get('username'),
        password=request_post.get('password')
    )
    if user is None:
        raise CustomException('Invalid Credentials!')
    return user


def get_user_by_name(name):
    return User.objects.filter(
        username=name
    ).first()


class CustomException(Exception):
    pass
