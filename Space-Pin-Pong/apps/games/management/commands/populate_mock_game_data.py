# app_name/management/commands/populate_data.py
from datetime import datetime, timezone

from apps.games.models import (GameHistory, GameMode, RemoteGameInfo,
                               Tournament, TournamentGame)
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Populate the database with fake data"

    def handle(self, *args, **kwargs):
        User.objects.create(user_id="olivia", nickname="nick")
        User.objects.create(user_id="totoro", nickname="nick")
        User.objects.create(user_id="mike", nickname="nick")
        User.objects.create(user_id="jane", nickname="nick")
        game = GameHistory.objects.create(
            start_time=datetime(2024, 1, 3, 11, 42, tzinfo=timezone.utc),
            end_time=datetime(2024, 1, 3, 12, 42, tzinfo=timezone.utc),
            game_mode=GameMode.REMOTE.value,
        )
        RemoteGameInfo.objects.create(game=game, user=User.objects.get(user_id="olivia"), score=100, is_winner=True)
        RemoteGameInfo.objects.create(game=game, user=User.objects.get(user_id="totoro"), score=10, is_winner=False)
        tournament = Tournament.objects.create(
            created_at=datetime(2024, 1, 4, 11, 42, tzinfo=timezone.utc),
            ended_at=datetime(2024, 1, 4, 12, 42, tzinfo=timezone.utc),
        )
        game = GameHistory.objects.create(
            start_time=datetime(2024, 1, 4, 11, 42, tzinfo=timezone.utc),
            end_time=datetime(2024, 1, 4, 12, 42, tzinfo=timezone.utc),
            game_mode=GameMode.TOURNAMENT.value,
        )
        TournamentGame.objects.create(game=game, tournament=tournament, round_number=4)
        RemoteGameInfo.objects.create(game=game, user=User.objects.get(user_id="olivia"), score=100, is_winner=True)
        RemoteGameInfo.objects.create(game=game, user=User.objects.get(user_id="totoro"), score=10, is_winner=False)
        game = GameHistory.objects.create(
            start_time=datetime(2024, 1, 4, 12, 42, tzinfo=timezone.utc),
            end_time=datetime(2024, 1, 4, 13, 42, tzinfo=timezone.utc),
            game_mode=GameMode.TOURNAMENT.value,
        )
        TournamentGame.objects.create(game=game, tournament=tournament, round_number=4)
        RemoteGameInfo.objects.create(game=game, user=User.objects.get(user_id="mike"), score=15, is_winner=True)
        RemoteGameInfo.objects.create(game=game, user=User.objects.get(user_id="jane"), score=1, is_winner=False)
        game = GameHistory.objects.create(
            start_time=datetime(2024, 1, 4, 13, 42, tzinfo=timezone.utc),
            end_time=datetime(2024, 1, 4, 14, 42, tzinfo=timezone.utc),
            game_mode=GameMode.TOURNAMENT.value,
        )
        TournamentGame.objects.create(game=game, tournament=tournament, round_number=2)
        RemoteGameInfo.objects.create(game=game, user=User.objects.get(user_id="olivia"), score=151, is_winner=True)
        RemoteGameInfo.objects.create(game=game, user=User.objects.get(user_id="mike"), score=10, is_winner=False)

        self.stdout.write(self.style.SUCCESS("Successfully populated the database with fake data!"))
