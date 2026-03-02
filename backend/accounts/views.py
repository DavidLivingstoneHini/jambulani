"""
Auth views — all token material is delivered via HttpOnly cookies.
The access token is ALSO returned in the JSON body for SSR/hydration.
"""
from __future__ import annotations

from django.conf import settings
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import JWTAuthentication
from .models import RefreshToken, User
from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)
from .tokens import issue_access_token, REFRESH_TOKEN_TTL_DAYS


def _get_client_ip(request: Request) -> str | None:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _set_auth_cookies(response: Response, access_token: str, raw_refresh: str, secure: bool) -> None:
    """Write both tokens as HttpOnly cookies."""
    response.set_cookie(
        "access_token",
        access_token,
        max_age=15 * 60,
        httponly=True,
        secure=secure,
        samesite="Lax",
        path="/",
    )
    response.set_cookie(
        "refresh_token",
        raw_refresh,
        max_age=REFRESH_TOKEN_TTL_DAYS * 24 * 3600,
        httponly=True,
        secure=secure,
        samesite="Lax",
        path="/api/v1/auth/",   # scope refresh cookie to auth endpoints only
    )


def _clear_auth_cookies(response: Response) -> None:
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/api/v1/auth/")


def _is_secure(request: Request) -> bool:
    return not settings.DEBUG


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth"

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()

        access = issue_access_token(user)
        rt_instance, raw_refresh = RefreshToken.issue(
            user=user,
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            ip_address=_get_client_ip(request),
        )

        data = {
            "user": UserProfileSerializer(user).data,
            "access_token": access,
        }
        response = Response(data, status=status.HTTP_201_CREATED)
        _set_auth_cookies(response, access, raw_refresh, _is_secure(request))
        return response


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth"

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data["user"]

        access = issue_access_token(user)
        rt_instance, raw_refresh = RefreshToken.issue(
            user=user,
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            ip_address=_get_client_ip(request),
        )

        data = {
            "user": UserProfileSerializer(user).data,
            "access_token": access,
        }
        response = Response(data, status=status.HTTP_200_OK)
        _set_auth_cookies(response, access, raw_refresh, _is_secure(request))
        return response


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        raw_refresh = request.COOKIES.get("refresh_token")
        if raw_refresh:
            token_hash = RefreshToken.hash_token(raw_refresh)
            try:
                rt = RefreshToken.objects.get(token_hash=token_hash, user=request.user)
                # Revoke the entire family
                RefreshToken.revoke_family(rt.family)
            except RefreshToken.DoesNotExist:
                pass  # Already revoked or invalid — still clear cookies

        response = Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
        _clear_auth_cookies(response)
        return response


class TokenRefreshView(APIView):
    """
    Refresh token rotation:
    - Accepts the refresh token from the HttpOnly cookie
    - Validates it, issues new access + refresh tokens
    - Detects reuse (token already rotated) → revokes entire family
    """
    permission_classes = [permissions.AllowAny]
    throttle_scope = "auth"

    def post(self, request: Request) -> Response:
        raw_refresh = request.COOKIES.get("refresh_token")
        if not raw_refresh:
            return Response({"detail": "Refresh token missing."}, status=status.HTTP_401_UNAUTHORIZED)

        token_hash = RefreshToken.hash_token(raw_refresh)

        try:
            rt = RefreshToken.objects.select_related("user").get(token_hash=token_hash)
        except RefreshToken.DoesNotExist:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

        # Reuse detection: token was already rotated → revoke entire family
        if rt.replaced_by_id is not None or rt.revoked:
            RefreshToken.revoke_family(rt.family)
            response = Response(
                {"detail": "Refresh token already used. Please log in again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            _clear_auth_cookies(response)
            return response

        if rt.is_expired:
            rt.revoked = True
            rt.save(update_fields=["revoked"])
            response = Response({"detail": "Refresh token expired."}, status=status.HTTP_401_UNAUTHORIZED)
            _clear_auth_cookies(response)
            return response

        user = rt.user
        if not user.is_active:
            return Response({"detail": "Account deactivated."}, status=status.HTTP_401_UNAUTHORIZED)

        # Issue new tokens (same family → enables reuse detection)
        new_access = issue_access_token(user)
        new_rt, new_raw_refresh = RefreshToken.issue(
            user=user,
            family=rt.family,
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            ip_address=_get_client_ip(request),
        )

        # Mark old token as rotated
        rt.replaced_by = new_rt
        rt.revoked = True
        rt.save(update_fields=["replaced_by", "revoked"])

        data = {
            "user": UserProfileSerializer(user).data,
            "access_token": new_access,
        }
        response = Response(data, status=status.HTTP_200_OK)
        _set_auth_cookies(response, new_access, new_raw_refresh, _is_secure(request))
        return response


class MeView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Clear cookies — force re-login after password change
        response = Response({"detail": "Password changed. Please log in again."})
        _clear_auth_cookies(response)
        return response


class SessionStatusView(APIView):
    """
    Lightweight endpoint called on app mount to check current auth state.
    Returns user info if the access_token cookie is valid, else 401.
    Does NOT try to refresh — the frontend handles that separately.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response({"user": UserProfileSerializer(request.user).data})
