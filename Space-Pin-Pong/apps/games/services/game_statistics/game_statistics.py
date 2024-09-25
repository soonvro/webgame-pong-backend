from apps.games.models import GameMode, RemoteGameInfo, TournamentGame
from django.contrib.auth import get_user_model

User = get_user_model()


def get_remote_game_ratio(user_id: str) -> list[int]:
    user = User.objects.get(user_id=user_id)
    total_games = (
        RemoteGameInfo.objects.where_game_mode(GameMode.REMOTE).filter(user=user).count()  # type: ignore[attr-defined]
    )
    win_games = (
        RemoteGameInfo.objects.where_game_mode(GameMode.REMOTE)  # type: ignore[attr-defined]
        .filter(user=user, is_winner=True)
        .count()
    )
    lose_games = total_games - win_games
    return [win_games, lose_games]


def get_tournament_ratio(user_id: str) -> list[int]:
    user = User.objects.get(user_id=user_id)
    total_games = (
        RemoteGameInfo.objects.where_game_mode(GameMode.TOURNAMENT)  # type: ignore[attr-defined]
        .filter(user=user)
        .count()
    )
    winning_round_2 = (
        TournamentGame.objects.where_round_number(2)  # type: ignore[attr-defined]
        .filter(game__remotegameinfo__user__user_id=user_id, game__remotegameinfo__is_winner=True)
        .count()
    )
    winning_round_4 = (
        TournamentGame.objects.where_round_number(4)  # type: ignore[attr-defined]
        .filter(game__remotegameinfo__user__user_id=user_id, game__remotegameinfo__is_winner=True)
        .count()
    )
    lose_round_4 = total_games - winning_round_2 - winning_round_4

    return [winning_round_2, winning_round_4 - winning_round_2, lose_round_4]
