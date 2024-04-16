from django.urls import path

from . import views

app_name = "chat_demo"

urlpatterns = [
    path("", views.chat, name="chat"),
]
