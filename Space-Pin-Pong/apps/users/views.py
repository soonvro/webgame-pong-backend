from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializer,
    UserDeleteSerializer,
    UserUpdateNicknameSerializer, 
    UserUpdatePictureSerializer,
    FriendListSerializer,
)
from .utils import get_user_from_token, get_user_from_id
from config import exceptions
from .models import User, Friend

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_user_from_id(user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        user = get_user_from_token(request)
        serializer = UserDeleteSerializer(user, data={'activated': False})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise exceptions.InvalidDataProvided

# game 모델 추가 후 수정 필요
class UserHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    pass

class UserNicknameUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = get_user_from_token(request)

        serializer = UserUpdateNicknameSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        raise exceptions.InvalidDataProvided

class UserPictureUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = get_user_from_token(request)

        serializer = UserUpdatePictureSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        raise exceptions.InvalidDataProvided

class UserFriendsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_user_from_token(request)

        friends_as_user1 = Friend.objects.filter(user1=user)
        friends_as_user2 = Friend.objects.filter(user2=user)

        all_friends = friends_as_user1 | friends_as_user2

        serialized_friends = FriendListSerializer(all_friends, many=True, context={'request': request}).data

        return Response({'friends_list': serialized_friends})


class UserFriendAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, friend_id):
        user = get_user_from_token(request)

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

class UserFriendDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, friend_id):
        user = get_user_from_token(request)

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