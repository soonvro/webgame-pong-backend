from channels.generic.websocket import AsyncWebsocketConsumer
import json
from . import utils

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        await self.channel_layer.group_add(
            f'notification_{self.user.user_id}',
            self.channel_name,
        )

        await self.accept()
        await self.send_pending_notifications()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'notification_{self.user.user_id}',
            self.channel_name,
        )

    async def send_pending_notifications(self):
        # 처리되지 않은 알림들을 전송
        notification_list = await utils.get_notifications(self.user)
        self.send(text_data=json.dumps({
            'type': 'notifications',
            'data': notification_list
        }))