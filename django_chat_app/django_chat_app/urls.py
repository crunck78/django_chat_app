"""django_chat_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from chat.views import (
    base,
    index,
    login_chat,
    register_chat,
    logout_chat,
    password_forgot,
    delete_message,
    post_message,
    search_users,
    request_chat,
    create_account,
    handle_login,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_chat),
    path('create-account/', create_account),
    path('login/', login_chat),
    path('handle-login', handle_login),
    path('logout/', logout_chat),
    path('', base),
    path('search-users/', search_users),
    path('request-chat/', request_chat),
    path('chat/', index),
    path('message-post/', post_message),
    path('message-delete/', delete_message),

    path('password-forgot/', password_forgot)
]
