"""
Accounts admin — rich user management with session/token visibility.
"""
from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count, QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import RefreshToken, User


def _badge(text: str, colour: str) -> str:
    return format_html(
        '<span style="background:{};color:#fff;padding:2px 10px;border-radius:20px;'
        'font-size:11px;font-weight:600;letter-spacing:.4px">{}</span>',
        colour, text,
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["-date_joined"]
    list_display = [
        "email", "full_name", "date_joined",
        "active_badge", "staff_badge", "token_count",
    ]
    list_display_links = ["email"]
    list_filter  = ["is_staff", "is_active", "date_joined"]
    search_fields = ["email", "first_name", "last_name"]
    readonly_fields = ["date_joined", "last_login", "full_name"]
    date_hierarchy = "date_joined"
    actions = ["activate_users", "deactivate_users"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "full_name", "phone")}),
        (_("Shipping address"), {
            "fields": ("address_line1", "address_line2", "city", "postal_code", "country"),
            "classes": ("collapse",),
        }),
        (_("Permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        (_("Timestamps"), {
            "fields": ("date_joined", "last_login"),
            "classes": ("collapse",),
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name", "last_name",
                "password1", "password2",
                "is_staff", "is_active",
            ),
        }),
    )

    @admin.display(description="Name")
    def full_name(self, obj: User) -> str:
        return obj.full_name or "—"

    @admin.display(description="Active")
    def active_badge(self, obj: User) -> str:
        return _badge("Active", "#16a34a") if obj.is_active else _badge("Inactive", "#dc2626")

    @admin.display(description="Role")
    def staff_badge(self, obj: User) -> str:
        if obj.is_superuser:
            return _badge("Superuser", "#7c3aed")
        if obj.is_staff:
            return _badge("Staff", "#2563eb")
        return _badge("Customer", "#6b7280")

    @admin.display(description="Active Sessions")
    def token_count(self, obj: User) -> str:
        count = obj._active_tokens  # annotated in get_queryset
        if count == 0:
            return format_html('<span style="color:#9ca3af">0</span>')
        return format_html('<span style="color:#16a34a;font-weight:600">{}</span>', count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            _active_tokens=Count(
                "refresh_tokens",
                filter=__import__("django.db.models", fromlist=["Q"]).Q(
                    refresh_tokens__revoked=False
                ),
            )
        )

    @admin.action(description="✓  Activate selected users")
    def activate_users(self, request: HttpRequest, qs: QuerySet) -> None:
        updated = qs.update(is_active=True)
        self.message_user(request, f"{updated} user(s) activated.")

    @admin.action(description="✕  Deactivate selected users")
    def deactivate_users(self, request: HttpRequest, qs: QuerySet) -> None:
        updated = qs.update(is_active=False)
        self.message_user(request, f"{updated} user(s) deactivated.")


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display  = ["user", "status_badge", "ip_address", "created_at", "expires_at"]
    list_display_links = ["user"]
    list_filter   = ["revoked", "created_at"]
    search_fields = ["user__email", "ip_address", "family"]
    readonly_fields = ["token_hash", "family", "created_at", "replaced_by", "user_agent", "ip_address"]
    date_hierarchy  = "created_at"
    ordering = ["-created_at"]

    @admin.display(description="Status")
    def status_badge(self, obj: RefreshToken) -> str:
        if obj.revoked:
            return _badge("Revoked", "#dc2626")
        if obj.is_expired:
            return _badge("Expired", "#d97706")
        return _badge("Valid", "#16a34a")

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False  # Tokens are issued programmatically only
