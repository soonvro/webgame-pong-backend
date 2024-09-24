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
    start_time: models.DateTimeField = models.DateTimeField()
    end_time: models.DateTimeField = models.DateTimeField()
    game_mode: models.CharField = models.CharField(
        max_length=20,
        choices=GameMode.choices(),
        default=GameMode.LOCAL.value,
    )

    class Meta:
        db_table = "game_history"
        verbose_name = "게임 기록"
        verbose_name_plural = "게임 기록"


class RemoteGameInfoManager(models.Manager):
    def where_game_mode(self, game_mode: GameMode):
        return self.filter(game__game_mode=game_mode.value)


class RemoteGameInfo(models.Model):
    game: models.ForeignKey = models.ForeignKey("GameHistory", on_delete=models.CASCADE)
    user: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score: models.IntegerField = models.IntegerField()
    is_winner: models.BooleanField = models.BooleanField()

    objects = RemoteGameInfoManager()

    class Meta:
        db_table = "remote_game_info"
        verbose_name = "Remote Game Info"
        verbose_name_plural = "Remote Game Info"


class LocalGameInfo(models.Model):
    game: models.OneToOneField = models.OneToOneField("GameHistory", on_delete=models.CASCADE)
    user: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_score: models.IntegerField = models.IntegerField()
    opponent_name: models.CharField = models.CharField(max_length=255, default="anonymous")
    opponent_score: models.IntegerField = models.IntegerField()

    class Meta:
        db_table = "local_game_info"
        verbose_name = "Local Game Info"
        verbose_name_plural = "Local Game Info"


class Tournament(models.Model):
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    ended_at: models.DateTimeField = models.DateTimeField(null=True)

    class Meta:
        db_table = "tournament"
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"


class TournamentGameManager(models.Manager):
    def where_round_number(self, round_number: int):
        if round_number not in TournamentGame.ROUNDS:
            raise ValueError(f"Round number must be one of {TournamentGame.ROUNDS}")
        return self.filter(round_number=round_number)


class TournamentGame(models.Model):
    game: models.ForeignKey = models.ForeignKey("GameHistory", on_delete=models.CASCADE)
    tournament: models.ForeignKey = models.ForeignKey("Tournament", on_delete=models.CASCADE)
    round_number: models.IntegerField = models.IntegerField()

    ROUNDS = [2, 4]

    objects = TournamentGameManager()

    class Meta:
        db_table = "tournament_game"
        verbose_name = "Tournament Game"
        verbose_name_plural = "Tournament Games"

    # validate round_number
    def save(self, *args, **kwargs):
        self.validate_round_number()
        super().save(*args, **kwargs)

    def validate_round_number(self):
        if self.round_number not in self.ROUNDS:
            raise ValueError(f"Round number must be one of {self.ROUNDS}")
