from django.db import models
from apps.users.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('alert.request', '요청 알림'),
        ('alert.basic', '기본 알림')
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)