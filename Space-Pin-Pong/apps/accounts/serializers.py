from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def to_internal_value(self, data):
        data_copy = data.copy()
        data_copy['refresh'] = data_copy.get('refresh_token')

        return super().to_internal_value(data_copy)

    def validate(self, attrs):
        data = super().validate(attrs)

        token = {
            'refresh_token': data.get('refresh'),
            'access_token': data['access'],
        }

        return {
            'message': '토큰 갱신 성공',
            'data': token,
        }
