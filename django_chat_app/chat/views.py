from django.core import serializers
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
    HttpResponseRedirect
)
from django.shortcuts import render

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from chat.utils import (
    get_conversation,
    get_requester_chats,
    get_searched_users,
    validate_registration,
    register_new_user,
    validate_login,
    validate_chatroom,
    validate_delete_message,
    validate_new_message,
    CustomException
)


@csrf_exempt
@require_http_methods(["GET"])
def register_chat(request):
    """
    Renders the registration page
    """
    redirect = request.GET.get('next')
    return render(request, 'auth/register.html', {'next': redirect})


@csrf_exempt
@require_http_methods(["POST"])
def create_account(request):
    """
    Creates a new user and logs it in
    """
    try:
        validate_registration(request.POST)
        user = register_new_user(request.POST)
        login(request, user)
        redirect = request.POST.get('next') or '/'
        return HttpResponseRedirect(redirect_to=redirect)
    except CustomException as err:
        return HttpResponseBadRequest(
            err,
            content_type="text/plain"
        )


@csrf_exempt
@require_http_methods(["GET"])
def login_chat(request):
    """
    Renders the login page
    """
    redirect = request.GET.get('next')
    return render(request, 'auth/login.html', {'next': redirect})


@csrf_exempt
@require_http_methods(["POST"])
def handle_login(request):
    """
    Authenticates the user
    """
    try:
        user = validate_login(request.POST)
        login(request, user)
        redirect = request.POST.get('next') or '/'
        return HttpResponseRedirect(redirect_to=redirect)
    except CustomException as err:
        return HttpResponseBadRequest(
            err,
            content_type="text/plain"
        )


@login_required(login_url='/login/')
@require_http_methods(["GET"])
def base(request):
    """
    Renders the  Base View
    """
    chats = get_requester_chats(request.user)
    return render(request, 'base.html', {'chats': chats})


@csrf_exempt
@login_required(login_url='/login/')
@require_http_methods(["GET"])
def logout_chat(request):
    """
    Logs user out
    """
    # Note that logout() doesn’t throw any errors if the user wasn’t logged in.
    logout(request)
    return HttpResponseRedirect('/login/')


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def search_users(request):
    """
    Returns a list of all Users
    that matches the search POST
    """
    try:
        searched_list = get_searched_users(request.POST['searchUsers'])
        return JsonResponse(searched_list, safe=False)
    except CustomException as err:
        return HttpResponseBadRequest(
            err,
            content_type="text/plain"
        )


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def request_chat(request):
    """
    Returns a redirection to the request chat
    """
    try:
        conversation = get_conversation(
            request.POST.get('userId'),
            request.user
        )
        return HttpResponseRedirect('chat/?id=' + str(conversation[0].pk))
    except CustomException as err:
        return HttpResponseBadRequest(
            err,
            content_type="text/plain"
        )


@login_required(login_url='/login/')
@require_http_methods(["GET"])
def index(request):
    """
    Renders Selected Chat Room
    """
    try:
        context = validate_chatroom(
            request.GET.get('id', None),
            request.user
        )
        return render(request, 'chat/index.html', context)
    except CustomException as err:
        return HttpResponseBadRequest(
            err,
            content_type="text/plain"
        )


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def delete_message(request):
    """
    Deletes a message from chat
    """
    try:
        validate_delete_message(request.POST.get('selected_message_id'))
        return HttpResponse(status=200)
    except CustomException as err:
        return HttpResponseBadRequest(
            err,
            content_type="text/plain"
        )


@login_required(login_url='/login/')
@require_http_methods(["POST"])
def post_message(request):

    # https://stackoverflow.com/questions/5895588/django-multivaluedictkeyerror-error-how-do-i-deal-with-it
    # print("Received data " + request.POST.get('textmessage', ''))
    # most likely errors report if POST[keyname] does not match

    try:
        new_message = validate_new_message(request.post)
        serializeMessage = serializers.serialize('json', [new_message, ])
        return JsonResponse(serializeMessage[1:-1], safe=False)
    except CustomException as err:
        return HttpResponseBadRequest(
            err,
            content_type="text/plain"
        )

# Be aware of UNIQUE constraint failed: auth_user.username
# https://stackoverflow.com/questions/47327406/django-error-unique-constraint-failed-auth-user-username


def password_forgot(request):
    redirect = request.GET.get('next')
    return render(request, 'auth/passwordForgot.html', {'next': redirect})
