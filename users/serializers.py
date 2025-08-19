from django.contrib.auth.models import User
from rest_framework import serializers
import uuid
from django.core.cache import cache
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer


SID_CACHE_KEY = "user:{user_id}:sid"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        sid = uuid.uuid4().hex
        cache.set(SID_CACHE_KEY.format(user_id=user.id), sid, None)
        token["sid"] = sid
        return token

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        incoming_refresh_str = attrs["refresh"]
        incoming_refresh = self.token_class(incoming_refresh_str)
        data = super().validate(attrs)

        user_id = incoming_refresh["user_id"]

        sid = uuid.uuid4().hex
        cache.set(SID_CACHE_KEY.format(user_id=user_id), sid, None)

        access = incoming_refresh.access_token
        access["sid"] = sid
        data["access"] = str(access)

        if "refresh" in data:
            new_refresh = self.token_class(data["refresh"])
            new_refresh["sid"] = sid
            data["refresh"] = str(new_refresh)
        else:
            data["refresh"] = incoming_refresh_str

        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
