from urllib import response
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

from django.contrib.auth.models import User

from .models import Message, Chat

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        # https://stackoverflow.com/questions/5895588/django-multivaluedictkeyerror-error-how-do-i-deal-with-it
        #print("Received data " + request.POST.get('textmessage', ''))
        # most likely errors report if POST[keyname] does not match
        print("Received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        newMessage = Message.objects.create(
            text=request.POST['textmessage'],
            chat=myChat,
            author=request.user,
            receiver=request.user
        )
        serializeMessage = serializers.serialize('json', [newMessage])
        return JsonResponse(serializeMessage[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})

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
            if(redirect == '/chat/'):  # For now we only need to redirect to chat
                return HttpResponseRedirect(request.POST.get('redirect'))
            else:
                return HttpResponseRedirect('/chat/')
        else:  # Handle invalid Credentials
            # Front End expects a text Response
            return HttpResponseBadRequest("Username or Password incorrect!", content_type="text/plain")
    # Handle non POST Requests
    return render(request, 'auth/login.html', {'redirect': redirect})

def register_chat(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':   # Handle POST REQUEST
        # Handle User Complete Registration
        if request.POST.get('password') == request.POST.get('check_password'):
            # Create user
            user = User.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=request.POST.get('password')
            )
            # Login User
            login(request, user)
            # Redirect to chat
            if(redirect == '/chat/'):  # For now we only need to redirect to chat
                return HttpResponseRedirect(request.POST.get('redirect'))
            else:
                return HttpResponseRedirect('/chat/')
        else:  # Handle Passwort Check Failed
            # if this happens it is odd, Frontend also should do this check
            return HttpResponseBadRequest("Password does not Match!", content_type="text/plain")
    return render(request, 'auth/register.html', {'redirect': redirect})

    
def logout_chat(request):
    # Note that logout() doesn’t throw any errors if the user wasn’t logged in.
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/login/')
