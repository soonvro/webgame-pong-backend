from apps.games.views import retrieve_game_statistics
from django.urls import path

urlpatterns = [
    path("users/<str:user_id>/", retrieve_game_statistics, name="retrieve_game_statistics"),
]
