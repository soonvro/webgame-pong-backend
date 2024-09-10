from django.urls import re_path

from . import consumers

user_websocket_urlpatterns = [
    re_path(r"ws/user-status/", consumers.NotificationConsumer.as_asgi()),
]