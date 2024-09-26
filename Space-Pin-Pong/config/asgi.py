from django.core.asgi import get_asgi_application

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

from apps.notifications.authentication import JWTAuthMiddleware
from apps.notifications.routing import notification_websocket_urlpatterns
from apps.users.routing import user_websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTAuthMiddleware(
            AuthMiddlewareStack(URLRouter([*notification_websocket_urlpatterns, *user_websocket_urlpatterns]))
        ),
    }
)
