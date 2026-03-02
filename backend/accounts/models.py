import secrets
import hashlib
from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Shipping address (optional, pre-fills checkout)
    phone = models.CharField(max_length=30, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True, default="Spain")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip() or self.email


class RefreshToken(models.Model):
    """
    Opaque refresh tokens stored as SHA-256 hashes.
    Raw token is only exposed once at issuance.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="refresh_tokens")
    token_hash = models.CharField(max_length=64, unique=True, db_index=True)
    family = models.CharField(
        max_length=64,
        db_index=True,
        help_text="Tokens in the same rotation family. Reuse of any non-current token in the family revokes all.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)
    replaced_by = models.OneToOneField(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="replaces"
    )
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"RefreshToken({self.user.email}, expires={self.expires_at:%Y-%m-%d})"

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    @property
    def is_valid(self) -> bool:
        return not self.revoked and not self.is_expired

    @classmethod
    def hash_token(cls, raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode()).hexdigest()

    @classmethod
    def issue(
        cls,
        user: "User",
        family: str | None = None,
        ttl_days: int = 30,
        user_agent: str = "",
        ip_address: str | None = None,
    ) -> tuple["RefreshToken", str]:
        """Create a new refresh token. Returns (instance, raw_token)."""
        raw = secrets.token_urlsafe(48)
        token_hash = cls.hash_token(raw)
        if family is None:
            family = secrets.token_hex(16)
        instance = cls.objects.create(
            user=user,
            token_hash=token_hash,
            family=family,
            expires_at=timezone.now() + timedelta(days=ttl_days),
            user_agent=user_agent,
            ip_address=ip_address,
        )
        return instance, raw

    @classmethod
    def revoke_family(cls, family: str) -> int:
        """Revoke all tokens in a rotation family (theft detection)."""
        return cls.objects.filter(family=family, revoked=False).update(revoked=True)
