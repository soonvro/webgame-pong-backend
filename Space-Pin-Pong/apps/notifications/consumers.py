from channels.generic.websocket import WebsocketConsumer
import json
from . import utils

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]

        self.channel_layer.group_add(
            f'notification_{self.user.user_id}',
            self.channel_name,
        )

        self.accept()
        self.send_pending_notifications()

    def disconnect(self, close_code):
        self.channel_layer.group_discard(
            f'notification_{self.user.user_id}',
            self.channel_name,
        )

    def send_pending_notifications(self):
        # 처리되지 않은 알림들을 전송
        notification_list = utils.get_notifications(self.user)
        self.send(text_data=json.dumps({
            'type': 'notifications',
            'data': notification_list
        }))