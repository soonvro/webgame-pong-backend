import random
import string

import jwt
import requests
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User

# 참고자료 https://api.intra.42.fr/apidoc/guides/web_application_flow
class OAuthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_data = {
            "client_id": settings.OAUTH_CLIENT_ID,
            "redirect_uri": settings.OAUTH_REDIRECT_URI,
            "response_type": "code",
        }
        request_url = (
            f"{settings.OAUTH_AUTHORIZE_URL}?client_id={request_data['client_id']}"
            f"&redirect_uri={request_data['redirect_uri']}&response_type={request_data['response_type']}"
        )
        return Response({"redirect_url": request_url})

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response(
                {'error': 'authorization-code not found'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_data = self._get_access_token(code)
        if not token_data:
            return Response(
                {'error': 'failed to get access token'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')

        user_info = self._get_user_info(access_token)
        if not user_info:
            return Response(
                {'error': 'failed to get user info'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user = self._get_or_create_user(user_info)
        if isinstance(user, Response):
            return user
        
        token = self._create_jwt(user)
        if not token:
            return Response(
                {'error': 'failed to create json web token'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'token': token})

    def _get_access_token(self, code):
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.OAUTH_CLIENT_ID,
            "client_secret": settings.OAUTH_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.OAUTH_REDIRECT_URI,
        }
        response = requests.post(settings.OAUTH_TOKEN_URL, data=data)
        if response.status_code != 200:
            return None
        token_json = response.json()
        token_data = {
            "access_token": token_json.get("access_token"),
            "refresh_token": token_json.get("refresh_token"),
        }
        return token_data
    
    def _get_user_info(access_token):
        api_url = settings.OAUTH_USER_API_URL
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            return None
        user_info = response.json()
        return user_info

    def _get_or_create_user(self, user_info):
        user_id = user_info.get('login')
        nickname = user_info.get('login')
        picture = user_info.get('image', {}).get('link')

        user = User.objects.filter(user_id=user_id).first()
        if user is None:
            try:
                user = User.objects.create_user(user_id, nickname, picture)
                # cache.set(f"status_{user.user_id}", "new user", timeout=60)
            except (IntegrityError, ValidationError) as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return user

    def _create_jwt(self, user):
        payload = {
            'user_id': user.user_id,
            'nickname': user.nickname,
            'picture': user.picture,
        }

        try:
            token = jwt.encode(payload, settings.OAUTH_CLIENT_SECRET, algorithm='HS256')
            return token
        except jwt.exceptions.PyJWTError as e:
            return None