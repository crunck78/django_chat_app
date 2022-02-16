from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == 'POST':
        #https://stackoverflow.com/questions/5895588/django-multivaluedictkeyerror-error-how-do-i-deal-with-it
        #print("Received data " + request.POST.get('textmessage', ''))
        print("Received data "  + request.POST['textmessage']) #most likely errors report if POST[keyname] does not match
    return render(request, 'chat/index.html', {'username': 'Mihai'})
