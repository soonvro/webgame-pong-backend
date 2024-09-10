from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from config.settings import base as settings
import jwt
from apps.users.models import User
from config import exceptions
from channels.middleware import BaseMiddleware

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        raise exceptions.UserNotFound

class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string'].decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]

        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = await get_user(payload['user_id'])
                scope['user'] = user
            except jwt.ExpiredSignatureError:
                raise exceptions.TokenExpired
            except jwt.InvalidTokenError:
                raise exceptions.InvalidTokenProvided
        else:
            raise exceptions.TokenNotProvided

        return await super().__call__(scope, receive, send)
