from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from apps.notifications.routing import notification_websocket_urlpatterns
from apps.users.routing import user_websocket_urlpatterns
from apps.notifications.authentication import JWTAuthMiddleware

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthMiddleware(
            AuthMiddlewareStack(
                URLRouter([
                    *notification_websocket_urlpatterns,
                    *user_websocket_urlpatterns
                ])
            )
        ),
    }
)
