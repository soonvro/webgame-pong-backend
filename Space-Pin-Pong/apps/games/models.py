from enum import Enum

from django.conf import settings
from django.db import models


class GameMode(Enum):
    LOCAL = "local"
    REMOTE = "remote"
    TOURNAMENT = "tournament"

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples representing the choices of this Enum.
        (DB에 저장될 값, 사용자에게 표시할 값)
        """
        return [(key.value, key.value) for key in cls]


class GameHistory(models.Model):
    start_time = models.DateTimeField()  # type: ignore
    end_time = models.DateTimeField()  # type: ignore
    game_mode = models.CharField(  # type: ignore
        max_length=20,
        choices=GameMode.choices(),
        default=GameMode.LOCAL.value,
    )

    class Meta:
        db_table = "game_history"
        verbose_name = "게임 기록"
        verbose_name_plural = "게임 기록"


class RemoteGameInfo(models.Model):
    game: models.ForeignKey = models.ForeignKey("GameHistory", on_delete=models.CASCADE)
    user: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score: models.IntegerField = models.IntegerField()
    is_winner: models.BooleanField = models.BooleanField()

    class Meta:
        db_table = "remote_game_info"
        verbose_name = "Remote Game Info"
        verbose_name_plural = "Remote Game Info"
