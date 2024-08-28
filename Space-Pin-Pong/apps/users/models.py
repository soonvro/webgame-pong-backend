from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, user_id, nickname, picture):
        if not user_id:
            raise ValueError('Users must have an user_id')

        user = self.model(
            user_id=user_id,
            nickname=nickname,
            picture=picture
        )

        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, primary_key=True)
    nickname = models.CharField(max_length=20)
    picture = models.URLField(default='https://cdn.vectorstock.com/i/500p/93/68/rocket-glyph-icon-spaceship-isolated-vector-51249368.jpg')
    recommendation = models.IntegerField(default=0)
    activated = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['nickname', 'picture']

    objects = UserManager()

    class Meta:
        db_table = 'users_user'