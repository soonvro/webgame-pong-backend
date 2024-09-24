from typing import Any

from django.db.models import Subquery
from rest_framework import serializers

from .models import (GameHistory, GameMode, RemoteGameInfo, Tournament,
                     TournamentGame)
from .services.game_statistics.game_statistics import (get_remote_game_ratio,
                                                       get_tournament_ratio)


class RemoteGameInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="user.user_id")
    score = serializers.IntegerField()
    is_winner = serializers.BooleanField()

    class Meta:
        model = RemoteGameInfo
        fields = ["user_id", "score", "is_winner"]


class RemoteGameHistorySerializer(serializers.Serializer):
    date = serializers.SerializerMethodField()  # type: ignore

    def __init__(self, instance=None, target_id: str | None = None, **kwargs):
        super().__init__(instance=instance, **kwargs)
        if target_id is None:
            raise ValueError("target_id is required")
        self.target_id = target_id

    def get_date(self, obj) -> list[int]:
        return [
            obj.start_time.year,
            obj.start_time.month,
            obj.start_time.day,
            obj.start_time.hour,
            obj.start_time.minute,
        ]

    def to_representation(self, instance) -> dict:
        ret = super().to_representation(instance)
        target_info = (
            RemoteGameInfo.objects.where_game_mode(GameMode.REMOTE)  # type: ignore[attr-defined]
            .filter(game=instance, user__user_id=self.target_id)
            .first()
        )
        opponent_info = (
            RemoteGameInfo.objects.where_game_mode(GameMode.REMOTE)  # type: ignore[attr-defined]
            .filter(game=instance)
            .exclude(user__user_id=self.target_id)
            .first()
        )
        target_info_data = RemoteGameInfoSerializer(target_info).data
        opponent_info_data = RemoteGameInfoSerializer(opponent_info).data
        ret["player"] = [target_info_data["user_id"], opponent_info_data["user_id"]]
        ret["score"] = [target_info_data["score"], opponent_info_data["score"]]
        ret["winner"] = target_info_data["user_id"] if target_info_data["is_winner"] else opponent_info_data["user_id"]
        return ret


class TournamentGameHistorySerializer(serializers.Serializer):
    def to_representation(self, instance) -> dict:
        ret = {}
        player_info = RemoteGameInfo.objects.where_game_mode(GameMode.TOURNAMENT).filter(  # type: ignore[attr-defined]
            game_id=instance
        )
        player_info_data = RemoteGameInfoSerializer(player_info, many=True).data
        if len(player_info_data) != 2:
            raise ValueError("TournamentGameHistory should have exactly 2 players")
        ret["player"] = [data["user_id"] for data in player_info_data]
        ret["score"] = [data["score"] for data in player_info_data]
        ret["winner"] = (
            player_info_data[0]["user_id"] if player_info_data[0]["is_winner"] else player_info_data[1]["user_id"]
        )
        return ret


class TournamentSerializer(serializers.Serializer):
    date = serializers.SerializerMethodField()  # type: ignore

    def get_date(self, obj) -> list[int]:
        return [
            obj.created_at.year,
            obj.created_at.month,
            obj.created_at.day,
            obj.created_at.hour,
            obj.created_at.minute,
        ]

    def to_representation(self, instance) -> dict:
        ret = super().to_representation(instance)
        game_history_ids = TournamentGame.objects.filter(tournament_id=instance.id).values("game_id")
        game_history = GameHistory.objects.filter(id__in=Subquery(game_history_ids))
        game_history_data = TournamentGameHistorySerializer(game_history, many=True).data
        ret["game_record"] = game_history_data
        return ret


class GameStatisticsSerializer:
    @classmethod
    def get_statistics(cls, user_id: str) -> dict[str, Any]:
        user_games = RemoteGameInfo.objects.filter(user__user_id=user_id).values("game")
        tournaments = Tournament.objects.filter(tournamentgame__game__in=Subquery(user_games)).distinct()
        ret = {
            "target": user_id,
            "dual": RemoteGameHistorySerializer(
                GameHistory.objects.filter(game_mode=GameMode.REMOTE.value, remotegameinfo__user__user_id=user_id),
                target_id=user_id,
                many=True,
            ).data,
            "dual_ratio": get_remote_game_ratio(user_id),
            "tournament": TournamentSerializer(tournaments, many=True).data,
            "tournament_ratio": get_tournament_ratio(user_id),
        }
        return ret
