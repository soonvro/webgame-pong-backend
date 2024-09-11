import re

from config import exceptions
from rest_framework import serializers

from .models import Friend, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "nickname", "picture", "recommendation", "activated", "created_at", "updated_at"]


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["activated"]

    def update(self, instance, validated_data):
        instance.activated = validated_data.get("activated", instance.activated)
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["nickname", "picture"]

    def validate_nickname(self, value):
        # 닉네임이 3자 이상 30자 이하인지 확인
        if len(value) < 1 or len(value) > 20:
            raise exceptions.NicknameLengthInvalid

        # 닉네임이 허용된 문자만 포함하는지 확인
        if not re.match(r"^[a-zA-Z0-9_-]+$", value):
            raise exceptions.NicknameFormatInvalid
        return value


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ["user1", "user2", "status"]


class UserFriendDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="user_id")  # user_id를 id로 변경
    nickName = serializers.CharField(source="nickname")  # nickname을 nickName으로 변경
    online = serializers.BooleanField(default=True)  # 하드코딩된 값 추가

    class Meta:
        model = User
        fields = ["id", "nickName", "online"]


class FriendListSerializer(serializers.ModelSerializer):
    friend = UserFriendDetailSerializer(source="get_friend", read_only=True)

    class Meta:
        model = Friend
        fields = ["friend"]

    def to_representation(self, instance):
        # 현재 사용자 정보를 가져옵니다.
        request_user = self.context["request"].user

        # Friend 모델의 get_friend 메소드를 호출합니다.
        friend_user = instance.get_friend(request_user)

        # UserFriendDetailSerializer를 사용하여 직렬화합니다.
        serializer = UserFriendDetailSerializer(friend_user)

        # 직렬화된 데이터를 반환합니다.
        return serializer.data
