from channels.generic.websocket import WebsocketConsumer
import json
from . import utils
from asgiref.sync import async_to_sync

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]

        async_to_sync(self.channel_layer.group_add)(
            f'notification_{self.user.user_id}',
            self.channel_name,
        )

        self.accept()
        self.send_pending_notifications()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
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

    def notifications(self, event):
        # 알림을 전송
        self.send(text_data=json.dumps(event))