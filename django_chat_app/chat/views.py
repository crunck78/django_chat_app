from django.shortcuts import render

from .models import Message, Chat

# Create your views here.


def index(request):
    if request.method == 'POST':
        # https://stackoverflow.com/questions/5895588/django-multivaluedictkeyerror-error-how-do-i-deal-with-it
        #print("Received data " + request.POST.get('textmessage', ''))
        # most likely errors report if POST[keyname] does not match
        print("Received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(
            text=request.POST['textmessage'],
            chat=myChat,
            author=request.user,
            receiver=request.user
        )
    return render(request, 'chat/index.html', {'username': 'Mihai'})
