from rest_framework.exceptions import APIException
from rest_framework import status

class EmptyAuthorizationCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'authorization-code가 존재하지 않습니다.'
    default_code = '001'

class InvalidAuthorizationCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'authorization-code가 유효하지 않습니다.'
    default_code = '002'

class UserInformationFetchFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = '서버가 42 API로부터 유저 정보를 가져오는데 실패했습니다.'
    default_code = '003'

class UserNotRegistered(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '해당 유저는 등록되지 않은 유저입니다.'
    default_code = '004'

class JWTTokenCreationFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = '서버가 JWT 토큰을 생성하는데 실패했습니다.'
    default_code = '005'

class InvalidTokenProvided(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '유효하지 않은 토큰이 제공되었습니다.'
    default_code = '006'

class DatabaseFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = '서버가 데이터베이스 에러로 인해 작업을 수행하지 못했습니다.'
    default_code = '007'

class UserInformationNotExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '회원가입을 위한 정보가 존재하지 않습니다.'
    default_code = '008'

class UserRegistrationFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = '서버가 유저를 등록하는데 실패했습니다.'
    default_code = '009'

class UserFromTokenError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = '서버가 토큰으로부터 유저를 가져오는데 실패했습니다.'
    default_code = '010'