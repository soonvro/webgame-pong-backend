from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class UserInfoView(APIView):
    pass

class UserDeleteView(APIView):
    pass

class UserHistoryView(APIView):
    pass

class UserNicknameUpdateView(APIView):
    pass

class UserPictureUpdateView(APIView):
    pass

class UserFriendsListView(APIView):
    pass

class UserFriendAddView(APIView):
    pass

class UserFriendDeleteView(APIView):
    pass