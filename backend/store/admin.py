"""
Jambulani store admin.
"""
from __future__ import annotations

from django.contrib import admin
from django.db.models import Count, Sum, QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    CartItem,
    Category,
    Collection,
    League,
    NewsletterSubscriber,
    Patch,
    Product,
    ProductImage,
    SizeChart,
)


# Shared helpers
def _img(url: str, height: int = 48) -> str:
    return format_html(
        '<img src="{}" height="{}" style="border-radius:4px;object-fit:cover;" />',
        url,
        height,
    )


def _badge(text: str, colour: str) -> str:
    """Render a coloured pill badge."""
    return format_html(
        '<span style="background:{};color:#fff;padding:2px 10px;border-radius:20px;'
        'font-size:11px;font-weight:600;letter-spacing:.4px">{}</span>',
        colour,
        text,
    )


# League
@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display  = ["logo_thumb", "name", "slug", "product_count", "status_badge", "sort_order"]
    list_editable = ["sort_order"]
    list_display_links = ["name"]
    list_filter   = ["is_active"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["sort_order", "name"]

    fieldsets = (
        (None, {"fields": ("name", "slug", "is_active", "sort_order")}),
        ("Images", {"fields": ("logo", "image"), "classes": ("wide",)}),
    )

    @admin.display(description="Logo")
    def logo_thumb(self, obj: League) -> str:
        if obj.logo:
            return _img(obj.logo.url, 40)
        if obj.image:
            return _img(obj.image.url, 40)
        return "—"

    @admin.display(description="Products")
    def product_count(self, obj: League) -> int:
        return obj.products.filter(is_active=True).count()

    @admin.display(description="Status")
    def status_badge(self, obj: League) -> str:
        return _badge("Active", "#16a34a") if obj.is_active else _badge("Hidden", "#6b7280")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(_pc=Count("products"))


# Collection
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display  = ["image_thumb", "name", "slug", "product_count", "status_badge", "sort_order"]
    list_editable = ["sort_order"]
    list_display_links = ["name"]
    list_filter   = ["is_active"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["sort_order", "name"]

    @admin.display(description="Image")
    def image_thumb(self, obj: Collection) -> str:
        return _img(obj.image.url, 40) if obj.image else "—"

    @admin.display(description="Products")
    def product_count(self, obj: Collection) -> int:
        return obj.products.filter(is_active=True).count()

    @admin.display(description="Status")
    def status_badge(self, obj: Collection) -> str:
        return _badge("Active", "#16a34a") if obj.is_active else _badge("Hidden", "#6b7280")


# Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ["name", "slug", "parent", "league", "collection", "status_badge"]
    list_display_links = ["name"]
    list_filter   = ["is_active", "league", "collection"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["parent", "league", "collection"]

    @admin.display(description="Status")
    def status_badge(self, obj: Category) -> str:
        return _badge("Active", "#16a34a") if obj.is_active else _badge("Hidden", "#6b7280")


# Patch
@admin.register(Patch)
class PatchAdmin(admin.ModelAdmin):
    list_display  = ["patch_preview", "name", "extra_price_display", "status_badge"]
    list_display_links = ["name"]
    list_editable = []
    list_filter   = ["is_active"]
    search_fields = ["name"]

    @admin.display(description="Preview")
    def patch_preview(self, obj: Patch) -> str:
        return _img(obj.image.url, 40) if obj.image else "—"

    @admin.display(description="Extra price")
    def extra_price_display(self, obj: Patch) -> str:
        if obj.extra_price:
            return format_html("<strong>+€{}</strong>", obj.extra_price)
        return format_html('<span style="color:#6b7280">Free</span>')

    @admin.display(description="Status")
    def status_badge(self, obj: Patch) -> str:
        return _badge("Active", "#16a34a") if obj.is_active else _badge("Inactive", "#6b7280")


# Size Chart
@admin.register(SizeChart)
class SizeChartAdmin(admin.ModelAdmin):
    list_display  = ["name", "chart_preview", "description_snippet"]
    search_fields = ["name"]

    @admin.display(description="Chart Image")
    def chart_preview(self, obj: SizeChart) -> str:
        return _img(obj.image.url, 50) if obj.image else "—"

    @admin.display(description="Description")
    def description_snippet(self, obj: SizeChart) -> str:
        return (obj.description[:80] + "…") if len(obj.description) > 80 else obj.description or "—"


# Product images inline
class ProductImageInline(admin.TabularInline):
    model   = ProductImage
    extra   = 2
    fields  = ["image_preview", "image", "alt_text", "is_primary", "sort_order"]
    readonly_fields = ["image_preview"]
    ordering = ["sort_order"]

    @admin.display(description="Preview")
    def image_preview(self, obj: ProductImage) -> str:
        if obj.image:
            return _img(obj.image.url, 60)
        return "—"


# Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "primary_thumb",
        "name",
        "league",
        "price_display",
        "stock_display",
        "featured_badge",
        "status_badge",
        "created_at",
    ]
    list_display_links = ["name"]
    list_filter   = ["is_featured", "is_active", "league", "category", "collection"]
    search_fields = ["name", "description", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ["patches"]
    inlines   = [ProductImageInline]
    date_hierarchy = "created_at"
    ordering  = ["-created_at"]
    readonly_fields = ["discount_percentage_display", "created_at", "updated_at"]
    actions   = ["make_featured", "remove_featured", "mark_active", "mark_inactive"]

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "description"),
            "classes": ("wide",),
        }),
        ("Categorisation", {
            "fields": ("category", "league", "collection"),
        }),
        ("Pricing", {
            "fields": ("price", "original_price", "discount_percentage_display"),
            "description": "Set original_price higher than price to show a discount badge.",
        }),
        ("Customisation Options", {
            "fields": (
                "available_sizes",
                "patches",
                "size_chart",
                "allow_name_customization",
                "allow_number_customization",
            ),
        }),
        ("Inventory & Visibility", {
            "fields": ("stock", "is_featured", "is_active"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    # Custom columns
    @admin.display(description="Image")
    def primary_thumb(self, obj: Product) -> str:
        img = obj.images.filter(is_primary=True).first() or obj.images.first()
        return _img(img.image.url, 48) if img else "—"

    @admin.display(description="Price")
    def price_display(self, obj: Product) -> str:
        if obj.original_price and obj.original_price > obj.price:
            return format_html(
                '<span style="font-weight:700">€{}</span> '
                '<span style="text-decoration:line-through;color:#9ca3af;font-size:12px">€{}</span>',
                obj.price,
                obj.original_price,
            )
        return format_html("<strong>€{}</strong>", obj.price)

    @admin.display(description="Stock")
    def stock_display(self, obj: Product) -> str:
        if obj.stock == 0:
            return _badge("Out of stock", "#dc2626")
        if obj.stock <= 5:
            return _badge(f"Low: {obj.stock}", "#d97706")
        return format_html(
            '<span style="color:#16a34a;font-weight:600">{}</span>', obj.stock
        )

    @admin.display(description="Featured", boolean=False)
    def featured_badge(self, obj: Product) -> str:
        return _badge("★ Featured", "#7c3aed") if obj.is_featured else "—"

    @admin.display(description="Status")
    def status_badge(self, obj: Product) -> str:
        return _badge("Live", "#16a34a") if obj.is_active else _badge("Draft", "#6b7280")

    @admin.display(description="Discount")
    def discount_percentage_display(self, obj: Product) -> str:
        pct = obj.discount_percentage
        if pct:
            return _badge(f"Save {pct}%", "#16a34a")
        return "No discount"

    # Bulk actions
    @admin.action(description="★  Mark selected as Featured")
    def make_featured(self, request: HttpRequest, qs: QuerySet) -> None:
        updated = qs.update(is_featured=True)
        self.message_user(request, f"{updated} product(s) marked as featured.")

    @admin.action(description="☆  Remove Featured from selected")
    def remove_featured(self, request: HttpRequest, qs: QuerySet) -> None:
        updated = qs.update(is_featured=False)
        self.message_user(request, f"{updated} product(s) removed from featured.")

    @admin.action(description="✓  Publish selected products")
    def mark_active(self, request: HttpRequest, qs: QuerySet) -> None:
        updated = qs.update(is_active=True)
        self.message_user(request, f"{updated} product(s) published.")

    @admin.action(description="✕  Unpublish (draft) selected products")
    def mark_inactive(self, request: HttpRequest, qs: QuerySet) -> None:
        updated = qs.update(is_active=False)
        self.message_user(request, f"{updated} product(s) moved to draft.")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related(
            "league", "category", "collection"
        ).prefetch_related("images")


# Cart Items
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display  = [
        "product_thumb", "product", "size",
        "custom_name", "custom_number", "patch",
        "quantity", "subtotal_display", "created_at",
    ]
    list_display_links = ["product"]
    list_filter   = ["created_at", "size"]
    search_fields = ["product__name", "custom_name", "session_key"]
    readonly_fields = ["session_key", "created_at"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    @admin.display(description="")
    def product_thumb(self, obj: CartItem) -> str:
        img = obj.product.images.filter(is_primary=True).first() or obj.product.images.first()
        return _img(img.image.url, 36) if img else "—"

    @admin.display(description="Subtotal")
    def subtotal_display(self, obj: CartItem) -> str:
        return format_html("<strong>€{}</strong>", obj.subtotal)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


# Newsletter Subscribers
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display  = ["email", "subscribed_at", "status_badge"]
    list_display_links = ["email"]
    list_filter   = ["is_active", "subscribed_at"]
    search_fields = ["email"]
    date_hierarchy = "subscribed_at"
    ordering = ["-subscribed_at"]
    actions = ["reactivate", "deactivate"]

    @admin.display(description="Status")
    def status_badge(self, obj: NewsletterSubscriber) -> str:
        return _badge("Subscribed", "#16a34a") if obj.is_active else _badge("Unsubscribed", "#6b7280")

    @admin.action(description="✓  Re-activate selected subscribers")
    def reactivate(self, request: HttpRequest, qs: QuerySet) -> None:
        updated = qs.update(is_active=True)
        self.message_user(request, f"{updated} subscriber(s) re-activated.")

    @admin.action(description="✕  Deactivate selected subscribers")
    def deactivate(self, request: HttpRequest, qs: QuerySet) -> None:
        updated = qs.update(is_active=False)
        self.message_user(request, f"{updated} subscriber(s) deactivated.")


# Admin site branding
admin.site.site_header = mark_safe(
    '<span style="font-family:\'Barlow Condensed\',sans-serif;font-weight:800;'
    'letter-spacing:2px;font-size:22px">JAMBULANI</span>'
    '<span style="font-size:13px;font-weight:400;color:#9ca3af;margin-left:8px">Store Admin</span>'
)
admin.site.site_title  = "Jambulani Admin"
admin.site.index_title = "Store Management"
