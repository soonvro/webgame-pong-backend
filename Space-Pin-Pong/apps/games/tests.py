import json
from datetime import datetime, timezone

from apps.games.models import (GameHistory, GameMode, RemoteGameInfo,
                               Tournament, TournamentGame)
from apps.games.views import retrieve_game_statistics
from django.contrib.auth import get_user_model
from django.test import TestCase as DjangoTestCase
from rest_framework.test import APIRequestFactory, force_authenticate

User = get_user_model()


class GameStatisticsTestCase(DjangoTestCase):
    def setUp(self):
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

    def test_retrieve_game_statistics(self):
        factory = APIRequestFactory()
        user = User.objects.get(user_id="olivia")
        view = retrieve_game_statistics

        # Make an authenticated request to the view...
        request = factory.get("/games/users/olivia")
        force_authenticate(request, user=user)
        response = view(request, user_id="olivia")
        self.assertEqual(response.status_code, 200, response.data)
