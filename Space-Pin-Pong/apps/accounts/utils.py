import requests
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from config import exceptions

from apps.users.models import User

def get_access_token(code):
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.OAUTH_CLIENT_ID,
        "client_secret": settings.OAUTH_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.OAUTH_REDIRECT_URI,
    }
    response = requests.post(settings.OAUTH_TOKEN_URL, data=data)
    if response.status_code != 200:
        raise exceptions.InvalidAuthorizationCode
    access_token = response.json().get("access_token")
    return access_token

def get_user_info(access_token):
    api_url = settings.OAUTH_USER_API_URL
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        raise exceptions.UserInformationFetchFailed
    user_info = response.json()
    return user_info

def get_user(code, user_info):
    user_id = user_info.get('login')

    user = User.objects.filter(user_id=user_id).first()
    if user is None:
        cache.set(code, user_info, timeout=60*5)
        raise exceptions.UserNotFound
    if user.activated is False:
        raise exceptions.UserDeactivated
    return user

def create_user(user_info):
    user_id = user_info.get('login')
    nickname = user_info.get('login')
    picture = user_info.get('image', {}).get('link')

    user = User.objects.filter(user_id=user_id).first()
    if user is None:
        try:
            user = User.objects.create_user(user_id, nickname, picture)
        except (IntegrityError, ValidationError):
            raise exceptions.UserRegistrationFailed
    return user

def create_jwt(user):
    try:
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }
    except TokenError as e:
        raise exceptions.JWTTokenCreationFailed
    return token