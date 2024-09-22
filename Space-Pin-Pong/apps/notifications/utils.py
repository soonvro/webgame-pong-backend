from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from .models import Notification

channel_layer = get_channel_layer()

@database_sync_to_async
def create_and_send_notifications(user, message, notification_type):
    # 알림 데이터베이스에 저장
    notification = Notification.objects.create(
        user=user,
        type=notification_type,
        message=message
    )

    # 웹소켓이 연결되어 있는 경우 실시간 알림 전송
    channel_layer.group_send(
        f'notification_{user.user_id}',
        {
            'type': notification.type,
            'id': notification.id,
            'message': notification.message,
        }
    )

    return notification