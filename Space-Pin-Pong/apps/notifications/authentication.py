import jwt
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from config.settings import base as settings
from apps.users.models import User
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return None

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
                user = await get_user(payload["user_id"])
                if user is None:
                    await self.set_error(scope, "004", "해당 유저를 찾을 수 없습니다.")
                scope["user"] = user
            except jwt.ExpiredSignatureError:
                await self.set_error(scope, "011", "토큰이 만료되었습니다.")
            except jwt.InvalidTokenError:
                await self.set_error(scope, "006", "유효하지 않은 토큰이 제공되었습니다.")
        else:
            await self.set_error(scope, "006", "유효하지 않은 토큰이 제공되었습니다.")

        return await super().__call__(scope, receive, send)

    async def set_error(self, scope, error_code, error_message):
        error = {
            "error_code": error_code,
            "error_message": error_message
        }
        scope["error"] = error
        scope["user"] = AnonymousUser()