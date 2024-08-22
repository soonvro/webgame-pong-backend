import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import User
from config.exceptions import *

def get_user_from_id(user_id):
    try:
        return get_object_or_404(User, user_id=user_id, activated=True)
    except User.DoesNotExist:
        raise UserNotExists

def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Bearer '):
        raise InvalidTokenProvided
    token = auth_header.split(' ')[1]

    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token.get('user_id')
        return get_object_or_404(User, user_id=user_id)
    except jwt.ExpiredSignatureError:
        raise TokenExpired
    except jwt.DecodeError:
        raise InvalidTokenProvided
    except User.DoesNotExist:
        raise UserNotExists