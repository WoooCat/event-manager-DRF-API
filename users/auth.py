from django.core.cache import cache
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class SessionBoundJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        sid = validated_token.get("sid")
        if not sid:
            raise AuthenticationFailed("Token missing session binding", code="token_no_sid")
        current = cache.get(f"user:{user.id}:sid")
        if not current or current != sid:
            raise AuthenticationFailed("Token has been revoked", code="token_revoked")
        return user
