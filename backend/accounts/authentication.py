"""
Custom DRF authentication backend.
Reads the access token from either:
  1. Authorization: Bearer <token>  header  (preferred for API clients)
  2. access_token HttpOnly cookie           (for browser SSR / Nuxt)
"""
from __future__ import annotations

import jwt
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from .tokens import decode_access_token

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        raw = self._extract_token(request)
        if raw is None:
            return None  # anonymous — let permission classes decide

        try:
            payload = decode_access_token(raw)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Access token has expired.", code="token_expired")
        except jwt.InvalidTokenError as exc:
            raise AuthenticationFailed(f"Invalid access token: {exc}", code="token_invalid")

        if payload.get("type") != "access":
            raise AuthenticationFailed("Token type mismatch.", code="token_invalid")

        user_id = payload.get("sub")
        try:
            user = User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found or inactive.", code="user_not_found")

        return user, payload

    @staticmethod
    def _extract_token(request: Request) -> str | None:
        # 1. Authorization header
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:]
        # 2. HttpOnly cookie
        return request.COOKIES.get("access_token") or None

    def authenticate_header(self, request: Request) -> str:
        return 'Bearer realm="api"'
