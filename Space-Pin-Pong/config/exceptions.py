from rest_framework.exceptions import APIException
from rest_framework import status

class EmptyAuthorizationCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'authorization-code가 존재하지 않습니다.'
    default_code = '001'

class InvalidAuthorizationCode(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'authorization-code가 유효하지 않습니다.'
    default_code = '002'

class UserInformationFetchFailed(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = '서버가 42 API로부터 유저 정보를 가져오는데 실패했습니다.'
    default_code = '003'

class UserNotExists(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '해당 유저가 존재하지 않습니다.'
    default_code = '004'

class JWTTokenCreationFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = '서버가 JWT 토큰을 생성하는데 실패했습니다.'
    default_code = '005'

class InvalidTokenProvided(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
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

class TokenExpired(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '토큰이 만료되었습니다.'
    default_code = '011'

class InvalidDataProvided(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '유효하지 않은 데이터가 제공되었습니다.'
    default_code = '012'

class NicknameLengthInvalid(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '닉네임은 2자 이상 20자 이하로 설정해야 합니다.'
    default_code = '013'

class NicknameFormatInvalid(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '닉네임은 알파벳, 숫자, 밑줄, 하이픈만 사용할 수 있습니다.'
    default_code = '014'

class SelfFriendRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '자기 자신을 친구로 추가하거나 삭제할 수 없습니다.'
    default_code = '015'

class FriendAlreadyExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '이미 친구로 추가된 사용자입니다.'
    default_code = '016'

class FriendNotExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '친구로 추가되지 않은 사용자입니다.'
    default_code = '017'