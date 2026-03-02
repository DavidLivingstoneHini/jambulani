"""
Stateless JWT access tokens (short-lived, 15 min).
Stateful opaque refresh tokens (long-lived, 30 days) with rotation + reuse detection.
"""
from __future__ import annotations

import time
from datetime import timedelta
from typing import TYPE_CHECKING

import jwt
from django.conf import settings
from django.utils import timezone

if TYPE_CHECKING:
    from .models import User

ACCESS_TOKEN_TTL_SECONDS = 15 * 60          # 15 minutes
REFRESH_TOKEN_TTL_DAYS   = 30


def _secret() -> str:
    return settings.SECRET_KEY


def issue_access_token(user: "User") -> str:
    """Return a signed JWT access token."""
    now = int(time.time())
    payload = {
        "sub": str(user.pk),
        "email": user.email,
        "is_staff": user.is_staff,
        "iat": now,
        "exp": now + ACCESS_TOKEN_TTL_SECONDS,
        "type": "access",
    }
    return jwt.encode(payload, _secret(), algorithm="HS256")


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.
    Raises jwt.InvalidTokenError subclasses on failure.
    """
    return jwt.decode(token, _secret(), algorithms=["HS256"])
