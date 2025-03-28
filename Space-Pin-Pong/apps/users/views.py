from config import exceptions
from django.db.models import Q
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from .serializers import (
    UserSerializer,
    UserDeleteSerializer,
    UserUpdateSerializer,
    FriendListSerializer,
    FriendSerializer,
)
from config import exceptions
from .models import User, Friend
from apps.notifications.utils import create_and_send_notifications

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = User.objects.filter(user_id=user_id, activated=True).first()
        if not user:
            raise exceptions.UserNotFound
        serializer = UserSerializer(user)
        return Response({"message": "유저 정보 조회 성공", "data": serializer.data})


class UserDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        serializer = UserDeleteSerializer(user, data={"activated": False})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "계정 탈퇴 성공"}, status=status.HTTP_200_OK)
        raise exceptions.InvalidDataProvided

class UserRecommendView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id):
        user = User.objects.filter(user_id=user_id, activated=True).first()
        if user is None:
            raise exceptions.UserNotFound

        UserUpdateSerializer(user).update(user, {})

        return Response({"message": "유저 인기도 업데이트 성공"}, status=status.HTTP_200_OK)

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def put(self, request):
        user = request.user

        data = request.data.copy()
        if 'nickName' in data:
            data['nickname'] = data.get('nickName')
        serializer = UserUpdateSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "유저 정보 수정 성공", "data": serializer.data})
        raise exceptions.InvalidDataProvided


class UserFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        friends = Friend.objects.filter(Q(user1=user, status="accept") | Q(user2=user, status="accept"))

        serialized_friends = FriendListSerializer(friends, many=True, context={'request': request}).data

        return Response({"message": "친구 목록 전송 성공", "data": {"friendList": serialized_friends}})

    def post(self, request, friend_id):
        user = request.user

        try:
            friend = User.objects.get(user_id=friend_id)
        except User.DoesNotExist:
            raise exceptions.UserNotFound

        if user.user_id == friend_id:
            raise exceptions.SelfFriendRequest

        is_friend = Friend.objects.filter(Q(user1=friend, user2=user) | Q(user1=user, user2=friend)).first()
        if is_friend:
            if is_friend.status  == 'accept':
                raise exceptions.FriendAlreadyExists
            elif is_friend.status == 'pending':
                raise exceptions.FriendRequestAlreadySent
            elif is_friend.status == 'reject':
                serializer = FriendSerializer(is_friend, data={"status": "pending"}, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        else:
            Friend.objects.create(user1=user, user2=friend)

        create_and_send_notifications(friend, user, f'{user.nickname}#{user.user_id}님이 친구 요청을 보냈습니다.', 'alert.request.friend')

        return Response({"message": "친구 추가 요청 성공"}, status=status.HTTP_201_CREATED)

    def delete(self, request, friend_id):
        user = request.user

        try:
            friend = User.objects.get(user_id=friend_id)
        except User.DoesNotExist:
            raise exceptions.UserNotFound

        if user.user_id == friend_id:
            raise exceptions.SelfFriendRequest

        friendship = Friend.objects.filter(Q(user1=friend, user2=user) | Q(user1=user, user2=friend)).first()

        if not friendship:
            raise exceptions.FriendNotExists

        friendship.delete()
        return Response({"message": "친구 삭제 성공"}, status=status.HTTP_200_OK)
 
class FriendAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, friend_id):
        user = request.user
        friend = User.objects.filter(user_id=friend_id).first()
        if not friend:
            raise exceptions.UserNotFound

        if user.user_id == friend_id:
            raise exceptions.SelfFriendRequest

        friendship = Friend.objects.filter(Q(user1=friend, user2=user) | Q(user1=user, user2=friend)).first()
        if not friendship:
            raise exceptions.FriendNotExists

        if friendship.status != "pending":
            raise exceptions.FriendAlreadyExists

        serializer = FriendSerializer(friendship, data={"status": "accept"}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        create_and_send_notifications(friend, user, f'{user.nickname}#{user.user_id}님이 친구 요청을 수락했습니다.', 'alert.basic')

        return Response({"message": "친구 요청 수락 성공"}, status=status.HTTP_200_OK)


class FriendRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, friend_id):
        user = request.user
        friend = User.objects.filter(user_id=friend_id).first()
        if not friend:
            raise exceptions.UserNotFound

        if user.user_id == friend_id:
            raise exceptions.SelfFriendRequest

        friendship = Friend.objects.filter(Q(user1=friend, user2=user) | Q(user1=user, user2=friend)).first()
        if not friendship:
            raise exceptions.FriendNotExists

        if friendship.status != "pending":
            raise exceptions.FriendAlreadyExists

        serializer = FriendSerializer(friendship, data={'status': 'reject'}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        create_and_send_notifications(friend, user, f'{user.nickname}#{user.user_id}님이 친구 요청을 거절했습니다.', 'alert.basic')

        return Response({"message": "친구 요청 거절 성공"}, status=status.HTTP_200_OK)
