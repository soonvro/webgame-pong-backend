from django.db import DatabaseError
from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from config.exceptions import EmptyAuthorizationCode, InvalidTokenProvided, ValidationFailed, UserInformationNotExists, DatabaseFailed
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from . import utils

class LoginView(APIView):
    permission_classes = [AllowAny]

    # 42 OAuth 인증 페이지로의 redirect_url 반환
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
        return Response({"redirect_url": redirect_url})

    def post(self, request):
        code = request.data.get('code')
        if not code:
            raise EmptyAuthorizationCode

        access_token = utils.get_access_token(code)

        user_info = utils.get_user_info(access_token)

        user = utils.get_user(user_info)

        token = utils.create_jwt(user)
        return Response({'token': token}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            # 추후에 access_token을 10분간 redis 캐시에 블랙리스트 추가하는 방안 추가 예정
            access_token = request.data.get('access_token')
            if not refresh_token or not access_token:
                raise InvalidTokenProvided
            refresh_token.blacklist()
            access_token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except (InvalidToken, TokenError):
            raise InvalidTokenProvided
        except DatabaseError:
            raise DatabaseFailed

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            raise EmptyAuthorizationCode

        user_info = cache.get(code)
        if not user_info:
            raise UserInformationNotExists

        user = utils.create_user(user_info)

        token = utils.create_jwt(user)

        return Response({'token': token}, status=status.HTTP_200_OK)

class CustomTokenRefreshView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        new_token = utils.refresh_jwt(refresh_token)

        return Response({'token': new_token}, status=status.HTTP_200_OK)