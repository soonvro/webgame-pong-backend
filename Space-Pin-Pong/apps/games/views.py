from apps.games.serializers import GameStatisticsSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_game_statistics(request, user_id: str):
    data: dict = GameStatisticsSerializer.get_statistics(user_id)
    return Response({"message": "전적 조회를 성공하였습니다.", "data": data})
