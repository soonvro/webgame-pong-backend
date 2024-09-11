from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    async def disconnect(self, close_code):
        pass
