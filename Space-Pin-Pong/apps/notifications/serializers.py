from rest_framework import serializers
from apps.notifications.models import Notification
from config import exceptions

class NotificationUpdateSerializer(serializers.Serializer):
    class Meta:
        model = Notification
        fields = ['status']