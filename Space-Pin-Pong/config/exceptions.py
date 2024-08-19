from rest_framework.exceptions import APIException
from rest_framework import status

class EmptyAuthorizationCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'authorization-code가 필요합니다.'
    default_code = '001'

class InvalidAuthorizationCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'access-token을 가져오는데 실패했습니다.'
    default_code = '002'

class UserInformationFetchFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '42 API로부터 유저 정보를 가져오는데 실패했습니다.'
    default_code = '003'

class UserNotRegistered(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '회원가입이 필요합니다.'
    default_code = '004'

class JWTTokenCreationFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'JWT 토큰 생성에 실패했습니다.'
    default_code = '005'

class InvalidTokenProvided(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'refresh_token과 access_token을 모두 제공해야 합니다.'
    default_code = '006'

class LogoutFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = '로그아웃에 실패했습니다.'
    default_code = '007'

class UserInformationNotExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '회원가입을 위한 정보가 존재하지 않습니다.'
    default_code = '008'

class UserRegistrationFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '회원가입을 실패했습니다.'
    default_code = '009'
