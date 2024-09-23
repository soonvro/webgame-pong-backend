from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Notification
from config import exceptions

class NotificationUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        notification_id = request.data.get('id')

        notification_updated = Notification.objects.filter(user=user, status=False, id=notification_id).update(status=True)

        if not notification_updated:
            raise exceptions.NotificationNotFound
        
        return Response({"message": "알림 상태 업데이트 성공"}, status=status.HTTP_200_OK)