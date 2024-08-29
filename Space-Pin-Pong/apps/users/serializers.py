import re
from rest_framework import serializers
from .models import User, Friend
from config import exceptions

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'nickname', 'picture', 'recommendation', 'activated', 'created_at', 'updated_at']

class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['activated']

    def update(self, instance, validated_data):
        instance.activated = validated_data.get('activated', instance.activated)
        instance.save()
        return instance

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'picture']

    def validate_nickname(self, value):
        # 닉네임이 3자 이상 30자 이하인지 확인
        if len(value) < 1 or len(value) > 20:
            raise exceptions.NicknameLengthInvalid

        # 닉네임이 허용된 문자만 포함하는지 확인
        if not re.match(r'^[a-zA-Z0-9_-]+$', value):
            raise exceptions.NicknameFormatInvalid
        return value

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['user1', 'user2']

class FriendListSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = ['friend']

    def get_friend(self, obj):
        request_user = self.request.user

        if obj.user1 == request_user:
            friend = obj.user2
        elif obj.user2 == request_user:
            friend = obj.user1

        return UserSerializer(friend).data