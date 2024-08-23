from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# ------------------------------------------------------------------------------
#  CORS 설정
# ------------------------------------------------------------------------------
INSTALLED_APPS += [
    'corsheaders',
]

# CORS 미들웨어는 최상단에 위치해야 합니다.
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
] + MIDDLEWARE

CORS_ORIGIN_ALLOW_ALL = True
