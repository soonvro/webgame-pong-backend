from config import exceptions
from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from . import utils
from .serializers import CustomTokenRefreshSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_data = {
            "client_id": settings.OAUTH_CLIENT_ID,
            "redirect_uri": settings.OAUTH_REDIRECT_URI,
            "response_type": "code",
        }
        redirect_url = (
            f"{settings.OAUTH_AUTHORIZE_URL}?client_id={request_data['client_id']}"
            f"&redirect_uri={request_data['redirect_uri']}&response_type={request_data['response_type']}"
        )
        return Response({"message": "redirect url 생성 성공", "data": redirect_url})

    def post(self, request):
        code = request.data.get("code")
        if not code:
            raise exceptions.EmptyAuthorizationCode

        access_token = utils.get_access_token(code)
        user_info = utils.get_user_info(access_token)
        user = utils.get_user(code, user_info)
        token = utils.create_jwt(user)

        return Response({"message": "로그인 성공", "data": token}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
        except TokenError:
            raise exceptions.InvalidTokenProvided

        return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("code")
        if not code:
            raise exceptions.EmptyAuthorizationCode

        user_info = cache.get(code)
        if not user_info:
            raise exceptions.UserInformationNotExists

        user = utils.create_user(user_info)
        token = utils.create_jwt(user)

        return Response({"message": "회원가입 및 로그인 성공", "data": token}, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenViewBase):
    permission_classes = [AllowAny]

    serializer_class = CustomTokenRefreshSerializer
