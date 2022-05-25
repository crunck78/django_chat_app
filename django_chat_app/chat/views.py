import json
from lib2to3.pgen2.token import EQUAL
from random import choices
from urllib import response
from django.core import serializers
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound, JsonResponse

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

from django.contrib.auth.models import User

from .models import Message, Chat

from django.db.models import Q

# Create your views here.


@login_required(login_url='/login/')
def base(request):
    """
    Renders the  Base View or returns a list of all Users that matches the search POST
    """
    # Handle Pressumably Search for Users to Chat to
    if request.method == 'POST':
        if request.POST.get('searchUser'):
            # MultiValueDictKeyError
            # https://stackoverflow.com/questions/5895588/django-multivaluedictkeyerror-error-how-do-i-deal-with-it
            # Better use Django Forms

            # https://stackoverflow.com/questions/23139657/django-get-all-users
            searchUser = request.POST['searchUser']
            # 'QuerySet' object has no attribute '_meta'
            # https://stackoverflow.com/questions/45856557/queryset-object-has-no-attribute-meta

            # search for users were no chat created was
            # do not send passwords with users list
            searched = User.objects.filter(username__startswith=searchUser)

            # https://stackoverflow.com/questions/22490379/how-to-return-an-array-of-objects-in-a-django-model/22490689
            searched_list = serializers.serialize('json', searched)

            print(searched_list)
            return JsonResponse(searched_list, safe=False)
        if request.POST.get('userId'):

            print("Got value :" + request.POST.get('userId'))
            # find user, create a chat if not allready exist, and redirect to new created chat or existing one
            choice = User.objects.filter(pk=request.POST.get('userId'))[0]

            choiceCreator = Q(creator__username=choice.username)
            choiceChatter = Q(chatter__username=choice.username)
            userCreator = Q(creator__username=request.user.username)
            userChatter = Q(chatter__username=request.user.username)

            hasChat = Chat.objects.filter(
                choiceCreator & userChatter |
                choiceChatter & userCreator
            )
            print(hasChat)
            # does a chat exist between selected user and logged in user?
            if(hasChat.count() > 0):
                return HttpResponseRedirect('chat/?id=' + str(hasChat[0].pk))
            else:
                newChat = Chat.objects.create(
                    creator=request.user,
                    chatter=choice,
                )
                print(newChat)
                return HttpResponseRedirect('chat/?id=' + str(newChat.pk))
    objectsChat = Chat.objects
    created = objectsChat.filter(creator__username=request.user.username)
    chattet = objectsChat.filter(chatter__username=request.user.username)
    chats = created | chattet
    # print('chats : ', chats.count())
    # if chats:
    return render(request, 'base.html', {'chats': chats})
    # return render(request, 'base.html', {'chats' : []})


@login_required(login_url='/login/')
def index(request):
    # Handle Pressumably Chat Opened
    selected_chat = None
    if request.method == 'GET':

        objectsChat = Chat.objects
       
        created = objectsChat.filter(creator__username=request.user.username)
        chattet = objectsChat.filter(chatter__username=request.user.username)
        chats = created | chattet

        # print(chats)

        chatId = request.GET.get('id', None)
        if chatId:
            selected_chat = Chat.objects.get(id=chatId)
            creator = selected_chat.creator
            chatter = selected_chat.chatter

            # make sure selected chat has authenticated user as member
            if creator == request.user or chatter == request.user:
                messages = Message.objects.filter(chat=selected_chat).order_by('created_at')
                selected_chat = serializers.serialize('json', [selected_chat])
                # messages = serializers.serialize('json', messages)
                return render(request, 'chat/index.html', {'chats': chats, 'selected_chat': json.loads(selected_chat)[0], 'messages': messages, 'chatter':chatter})
            else:
                print('Trying to access a chat that does not belong to')
                return HttpResponseBadRequest(request)
        else:
            # return render(request, 'chat/index.html', {'chats': chats, 'selected_chat': None, 'messages': []})
            return HttpResponseBadRequest(request)
    # Handle Pressumably Message Receive
    if request.method == 'POST':
        # https://stackoverflow.com/questions/5895588/django-multivaluedictkeyerror-error-how-do-i-deal-with-it
        # print("Received data " + request.POST.get('textmessage', ''))
        # most likely errors report if POST[keyname] does not match
        print(request)
        print("Received data " + request.POST['textmessage'])

        myChat = Chat.objects.get(id=request.POST['selected_chat'])

        creator = myChat.creator
        chatter = myChat.chatter

        if creator == request.user:
            newMessage = Message.objects.create(
                text=request.POST['textmessage'],
                chat=myChat,
                author=request.user,  # ? can it not be
                receiver=chatter
            )
        if chatter == request.user:
            newMessage = Message.objects.create(
                text=request.POST['textmessage'],
                chat=myChat,
                author=request.user,  # ? can it not be
                receiver=creator
            )

            print(newMessage.created_at)

        serializeMessage = serializers.serialize('json', [newMessage,])
        return JsonResponse(serializeMessage[1:-1], safe=False)

    # objectsChat = Chat.objects
    # created = objectsChat.filter(creator__username=request.user.username)
    # chattet = objectsChat.filter(chatter__username=request.user.username)
    # chats = created | chattet
    # return render(request, 'chat/index.html', {'chats': chats})

# def getAllChats(user: User):
#     return Chat.objects.filter(creator__id=user.id)


def login_chat(request):
    # This can be None
    # Sure case: request.GET.get('next') = /chat/ if we got redirected from chat to login because of @login_require decorator
    # Unknown case: request.GET.get('next') = anything , should this be an issue?
    redirect = request.GET.get('next')
    if request.method == 'POST':  # Handle POST Request
       # Authenticate User
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user is not None:  # Handle Authenticate Successfully
            # Login User
            login(request, user)
            # Redirect to chat
            if(redirect):  # For now we only need to redirect to chat
                return HttpResponseRedirect(request.POST.get('redirect'))
            else:
                return HttpResponseRedirect('/')
        else:  # Handle invalid Credentials
            # Front End expects a text Response
            return HttpResponseBadRequest("Username or Password incorrect!", content_type="text/plain")
    # Handle non POST Requests
    return render(request, 'auth/login.html', {'redirect': redirect})

# Be aware of UNIQUE constraint failed: auth_user.username
# https://stackoverflow.com/questions/47327406/django-error-unique-constraint-failed-auth-user-username


def register_chat(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':   # Handle POST REQUEST
        # Handle User Complete Registration
        if request.POST.get('password') == request.POST.get('check_password'):
            # Create user
            if User.objects.filter(username=request.POST.get('username')).first():
                return HttpResponseBadRequest('This username is already taken')
           
            user = User.objects.create_user(
                username=request.POST.get('username'),
                # email=request.POST.get('email'),
                password=request.POST.get('password')
            )

            if user:
                # Login User
                login(request, user)
                # Redirect to chat
                if(redirect == '/chat/'):  # For now we only need to redirect to chat
                    return HttpResponseRedirect(request.POST.get('redirect'))
                else:
                    return HttpResponseRedirect('/chat/')
            else: 
                return HttpResponseBadRequest()
        else:  # Handle Passwort Check Failed
            # if this happens it is odd, Frontend also should do this check
            return HttpResponseBadRequest("Password does not Match!", content_type="text/plain")
    return render(request, 'auth/register.html', {'redirect': redirect})


def logout_chat(request):
    # Note that logout() doesn’t throw any errors if the user wasn’t logged in.
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/login/')
