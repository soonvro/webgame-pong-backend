from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, user_id, nickname, picture):
        if not user_id:
            raise ValueError("Users must have an user_id")

        user = self.model(user_id=user_id, nickname=nickname, picture=picture)

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, primary_key=True)
    nickname = models.CharField(max_length=20)
    picture = models.CharField(max_length=2083)
    recommendation = models.IntegerField(default=0)
    activated = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ["nickname", "picture"]

    objects = UserManager()


class Friend(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPT = 'accept'
    STATUS_REJECT = 'reject'

    FRIEND_STATUS_CHOICES = [
        (STATUS_PENDING, '보류 중'),
        (STATUS_ACCEPT, '수락'),
        (STATUS_REJECT, '거절'),
    ]

    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_as_user2')
    status = models.CharField(max_length=20, choices=FRIEND_STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user1", "user2"], name="unique_friend_pair")]

    def save(self, *args, **kwargs):
        if self.user1.user_id > self.user2.user_id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

    def get_friend(self, user):
        if self.user1 == user:
            return self.user2
        return self.user1
