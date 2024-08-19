from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
            return Response(
                {'error_message': 'authorization-code가 필요합니다.'},
                {'error_code': '001'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        access_token = utils.get_access_token(code)
        if not access_token:
            return Response(
                {'error_message': 'access-token을 가져오는데 실패했습니다.'},
                {'error_code': '002'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_info = utils.get_user_info(access_token)
        if not user_info:
            return Response(
                {'error_message': '42 API로부터 유저 정보를 가져오는데 실패했습니다.'},
                {'error_code': '003'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = utils.get_user(user_info)
        if not user:
            cache.set(code, user_info, timeout=60*10)
            return Response(
                {'error_message': '회원가입이 필요합니다.'},
                {'error_code': '004'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = utils.create_jwt(user)
        if not token:
            return Response(
                {'error_message': 'JWT 토큰 생성에 실패했습니다.'},
                {'error_code': '005'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response({'token': token}, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            # 추후에 access_token을 10분간 redis 캐시에 블랙리스트 추가하는 방안 추가 예정
            access_token = request.data.get('access_token')
            if not refresh_token or not access_token:
                return Response(
                    {'error_message': 'refresh_token과 access_token을 모두 제공해야 합니다.'},
                    {'error_code': '006'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            refresh_token.blacklist()
            access_token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error_message': '로그아웃에 실패했습니다.'},
                {'error_code': '007'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response(
                {'error_message': 'authorization-code가 필요합니다.'},
                {'error_code': '001'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_info = cache.get(code)
        if not user_info:
            return Response(
                {'error_message': '회원가입을 위한 정보가 존재하지 않습니다.'},
                {'error_code': '008'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = utils.create_user(user_info)
        if not user:
            return Response(
                {'error_message': '회원가입에 실패했습니다.'},
                {'error_code': '009'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = utils.create_jwt(user)
        if not token:
            return Response(
                {'error_message': 'JWT 토큰 생성에 실패했습니다.'},
                {'error_code': '005'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response({'token': token}, status=status.HTTP_200_OK)

class CustomTokenRefreshView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        new_token = utils.refresh_jwt(refresh_token)
        if not new_token:
            return Response(
                {'error_message': 'JWT 토큰 생성에 실패했습니다.'},
                {'error_code': '005'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({'token': new_token}, status=status.HTTP_200_OK)