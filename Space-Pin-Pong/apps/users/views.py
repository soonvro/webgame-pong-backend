from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializer,
    UserDeleteSerializer,
    UserUpdateSerializer,
    FriendListSerializer,
)
from config import exceptions
from .models import User, Friend

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        serializer = UserSerializer(user_id)
        return Response(serializer.data)

class UserDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        serializer = UserDeleteSerializer(user, data={'activated': False})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise exceptions.InvalidDataProvided

# game 모델 추가 후 수정 필요
class UserHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    pass

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        raise exceptions.InvalidDataProvided

class UserFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Q 객체를 사용하여 user1 또는 user2가 현재 사용자의 친구들을 필터링
        friends = Friend.objects.filter(
            Q(user1=user) | Q(user2=user)
        )

        # 직렬화하여 응답으로 반환
        serialized_friends = FriendListSerializer(friends, many=True, context={'request': request}).data

        return Response({'friends_list': serialized_friends})

    def post(self, request, friend_id):
        user = request.user

        try:
            friend = User.objects.get(user_id=friend_id)
        except User.DoesNotExist:
            raise exceptions.UserNotExists

        if user.user_id == friend_id:
            raise exceptions.SelfFriendRequest

        if user > friend:
            user, friend = friend, user

        if Friend.objects.filter(user1=user, user2=friend).exists():
            raise exceptions.FriendAlreadyExists

        Friend.objects.create(user1=user, user2=friend)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, friend_id):
        user = request.user

        try:
            friend = User.objects.get(user_id=friend_id)
        except User.DoesNotExist:
            raise exceptions.UserNotExists

        if user.user_id == friend_id:
            raise exceptions.SelfFriendRequest

        if user > friend:
            user, friend = friend, user

        friendship = Friend.objects.filter(user1=user, user2=friend).first()

        if not friendship:
            raise exceptions.FriendNotExists

        friendship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)