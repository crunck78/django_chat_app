import json

from django.core import serializers
from django.contrib.auth.models import User
from django.db.models import Q

from chat.models import Chat, Message

from django.contrib.auth import authenticate


def get_searched_users(request_search):
    """
    Returns a List of filtered Users,
    where username starts with request_search value
    """
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
    """
    Returns the Chat between User with id user_id and request_user
    If no such Chat exists, a new Chat is created
    """
    selected_user = get_user_by_id(user_id)
    query_chat = get_query_chat(selected_user, request_user)

    hasChat = Chat.objects.filter(
        query_chat['selected_creator'] & query_chat['user_chatter'] |
        query_chat['selected_chatter'] & query_chat['user_creator']
    )
    # does a chat exist between selected user and logged in user?
    if (hasChat.count() > 0):
        return hasChat[0]
    else:
        newChat = create_conversation(selected_user, request_user)
        return newChat


def get_user_by_id(user_id):
    """
    Returns the User Model where id equals user_id
    """
    try:
        return User.objects.get(id=user_id)
    except Exception as err:
        raise CustomException(err)


def get_query_chat(selected_user, request_user):
    """
    Returns a Dictionary to help filter for a list of Chats,
    between selected_user and request_user
    """
    return {
        "selected_creator": Q(creator__username=selected_user.username),
        "selected_chatter": Q(chatter__username=selected_user.username),
        "user_creator": Q(creator__username=request_user.username),
        "user_chatter": Q(chatter__username=request_user.username),
    }


def create_conversation(selected_user, request_user):
    """
    Creates a new Chat between selected_user and request_user
    """
    return Chat.objects.create(
        creator=request_user,
        chatter=selected_user,
    )


def validate_chatroom(chat_id, request_user):
    """
    Returns context for chat room if valid
    """
    selected_chat = get_chat_by_id(chat_id)

    validate_membership(request_user, selected_chat)
    creator = selected_chat.creator
    chatter = selected_chat.chatter
    messages = get_chat_messages(selected_chat)
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


def get_chat_messages(selected_chat):
    """
    Returns all Messages from selected_chat
    """
    return Message.objects.filter(chat=selected_chat).order_by('created_at')


def validate_delete_message(message_id, request_user):
    """
    Deletes a message if request user is a member of the message chat
    and request user is owner of message
    """
    message = Message.objects.get(id=message_id)
    validate_membership(request_user, message.chat)
    validate_message_owner(message, request_user)
    message.delete()


def validate_message_owner(message, request_user):
    """
    Raises exception if request_user is not the author of the message
    """
    author = message.author
    if author != request_user:
        raise CustomException(
            'This is not your message to delete!'
        )


def validate_new_message(request):
    """
    Creates new message if request user is member of the selected_chat
    """
    my_chat = get_chat_by_id(request.POST.get('selected_chat', None))
    validate_membership(request.user, my_chat)
    new_message = Message.objects.create(
        text=request.POST.get('textmessage'),
        chat=my_chat,
        author=request.user,  # ? can it not be
        receiver=my_chat.chatter
    )
    return new_message


def validate_membership(request_user, chat):
    """
    Raise exception if request_user is no member of the chat
    """
    creator = chat.creator
    chatter = chat.chatter
    if creator != request_user and chatter != request_user:
        raise CustomException(
            'This Chat does not exist or your are not a member of it!'
        )


def get_chat_by_id(chat_id):
    """
    Returns a Chat Model were id is equal to chat_id
    """
    try:
        return Chat.objects.get(id=chat_id)
    except Exception as err:
        raise CustomException(err)


def get_requester_chats(request_user):
    """
    Returns all Chats were request_user is a member
    """
    objects_chat = Chat.objects
    creator = objects_chat.filter(creator__username=request_user.username)
    chatter = objects_chat.filter(chatter__username=request_user.username)
    chats = creator | chatter
    return chats


def validate_registration(request_post):
    """
    Raises exception if Password check fails
    or user already exists
    """
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
    """
    Creates and return a new user by username and password
    """
    new_user = User.objects.create_user(
        username=request_post.get('username'),
        # email=request_post.get('email'),
        password=request_post.get('password')
    )
    return new_user


def validate_login(request_post):
    """
    Authenticates a user by username and password
    Raises exception if Credentials are invalid
    """
    user = authenticate(
        username=request_post.get('username'),
        password=request_post.get('password')
    )
    if user is None:
        raise CustomException('Invalid Credentials!')
    return user


def get_user_by_name(name):
    """
    Returns first user where username equals name
    """
    return User.objects.filter(
        username=name
    ).first()


class CustomException(Exception):
    """
    A Help Exception Class that just extends Exception
    """
    pass
