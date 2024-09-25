from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

class UserStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        await self.accept()
        cache.set(f'user_online_{self.user.user_id}', True)

    async def disconnect(self, close_code):
        cache.set(f'user_online_{self.user.user_id}', False)