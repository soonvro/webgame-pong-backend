from channels.layers import get_channel_layer
from .models import Notification
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

def create_and_send_notifications(user, from_user, message, notification_type):
    # 알림 데이터베이스에 저장
    Notification.objects.create(
        user=user,
        from_user=from_user,
        type=notification_type,
        message=message
    )

    notification_list = get_notifications(user)

    # 웹소켓이 연결되어 있는 경우 실시간 알림 전송
    async_to_sync(channel_layer.group_send)(
        f'notification_{user.user_id}',
        {
            'type': 'notifications',
            'data': notification_list
        }
    )

def get_notifications(user):
    # 알림을 리스트로 만들어 한 번에 전송하는 방식
    notification_list = []
    notifications = Notification.objects.filter(user=user, status=False)
    # 모든 알림을 리스트에 추가
    for notification in notifications:
        notification_list.append({
            'type': notification.type,
            'id': notification.id,
            'message': notification.message,
            'friendId': notification.from_user.user_id,
        })
    return notification_list