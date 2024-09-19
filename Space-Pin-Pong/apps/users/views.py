from django.db.models import Q
from rest_framework import status
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
from apps.notifications.utils import create_notification

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = User.objects.filter(user_id=user_id, activated=True).first()
        if not user:
            raise exceptions.UserNotFound
        serializer = UserSerializer(user)
        return Response({"message": "유저 정보 조회 성공" , "data": serializer.data})

class UserDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        serializer = UserDeleteSerializer(user, data={'activated': False})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "계정 탈퇴 성공"}, status=status.HTTP_204_NO_CONTENT)
        raise exceptions.InvalidDataProvided

# game 모델 추가 후 수정 필요
# class UserHistoryView(APIView):
#     permission_classes = [IsAuthenticated]
#     pass

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

        # Q 객체를 사용하여 user1 또는 user2가 현재 사용자의 친구들을 필터링
        friends = Friend.objects.filter(
            Q(user1=user, status='accept') | Q(user2=user, status='accept')
        )

        # 직렬화하여 응답으로 반환
        serialized_friends = FriendListSerializer(friends, many=True, context={'request': request}).data

        return Response({
            'message': '친구 목록 전송 성공',
            'data': {
                'friendList': serialized_friends
            }
        })

    def post(self, request, friend_id):
        user = request.user

        try:
            friend = User.objects.get(user_id=friend_id)
        except User.DoesNotExist:
            raise exceptions.UserNotFound

        if user.user_id == friend_id:
            raise exceptions.SelfFriendRequest

        if Friend.objects.filter(Q(user1=friend, user2=user) | Q(user1=user, user2=friend)).exists():
            raise exceptions.FriendAlreadyExists

        Friend.objects.create(user1=user, user2=friend)

        create_notification(friend, f'{user.nickname}#{user.user_id}님이 친구 요청을 보냈습니다.', 'alert.request')

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
        return Response({"message": "친구 삭제 성공"}, status=status.HTTP_204_NO_CONTENT)
 
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

        if friendship.status != 'pending':
            raise exceptions.FriendAlreadyExists

        serializer = FriendSerializer(friendship, data={'status': 'accept'}, partial=True).is_valid(raise_exception=True)

        if serializer.is_valid():
            serializer.save()
            create_notification(friend, f'{user.nickname}#{user.user_id}님이 친구 요청을 수락했습니다.', 'alert.basic')
            return Response({"message": "친구 요청 수락 성공"}, status=status.HTTP_200_OK)
        raise exceptions.InvalidDataProvided

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

        if friendship.status != 'pending':
            raise exceptions.FriendAlreadyExists

        serializer = FriendSerializer(friendship, data={'status': 'reject'}, partial=True).is_valid(raise_exception=True)

        if serializer.is_valid():
            serializer.save()
            create_notification(friend, f'{user.nickname}#{user.user_id}님이 친구 요청을 거절했습니다.', 'alert.basic')
            return Response({"message": "친구 요청 거절 성공"}, status=status.HTTP_200_OK)
        raise exceptions.InvalidDataProvided