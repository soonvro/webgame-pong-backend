from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import NotificationUpdateSerializer
from .models import Notification
from config import exceptions

class NotificationUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        notification_id = request.data.get('id')

        notification = Notification.objects.filter(user=user, status=False, id=notification_id).first()
        if not notification:
            raise exceptions.NotificationNotFound
        serializer = NotificationUpdateSerializer(notification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "알림 상태 업데이트 성공"})
        raise exceptions.InvalidDataProvided