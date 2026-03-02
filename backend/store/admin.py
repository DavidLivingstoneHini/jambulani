from django.contrib import admin
from django.utils.html import format_html
from .models import (
    League,
    Collection,
    Category,
    Patch,
    SizeChart,
    Product,
    ProductImage,
    CartItem,
    NewsletterSubscriber,
)


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active", "sort_order", "logo_preview"]
    list_editable = ["is_active", "sort_order"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" height="40" />', obj.logo.url)
        return "—"
    logo_preview.short_description = "Logo"


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active", "sort_order"]
    list_editable = ["is_active", "sort_order"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "parent", "league", "collection", "is_active"]
    list_editable = ["is_active"]
    list_filter = ["league", "collection"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Patch)
class PatchAdmin(admin.ModelAdmin):
    list_display = ["name", "extra_price", "is_active"]
    list_editable = ["is_active", "extra_price"]


@admin.register(SizeChart)
class SizeChartAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ["image", "alt_text", "is_primary", "sort_order"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name", "league", "category", "price", "original_price",
        "discount_percentage", "is_featured", "is_active", "stock", "created_at",
    ]
    list_editable = ["price", "original_price", "is_featured", "is_active", "stock"]
    list_filter = ["league", "category", "collection", "is_featured", "is_active"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ["patches"]
    inlines = [ProductImageInline]
    readonly_fields = ["discount_percentage", "created_at", "updated_at"]
    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "slug", "description", "category", "league", "collection"),
        }),
        ("Pricing", {
            "fields": ("price", "original_price", "discount_percentage"),
        }),
        ("Customization", {
            "fields": ("available_sizes", "patches", "size_chart",
                       "allow_name_customization", "allow_number_customization"),
        }),
        ("Inventory", {
            "fields": ("stock", "is_featured", "is_active"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def discount_percentage(self, obj):
        return f"{obj.discount_percentage}%"
    discount_percentage.short_description = "Discount"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["product", "size", "custom_name", "custom_number", "quantity", "subtotal", "created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["session_key", "subtotal"]


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "subscribed_at", "is_active"]
    list_editable = ["is_active"]
    search_fields = ["email"]


# Customize admin site
admin.site.site_header = "Jambulani Admin"
admin.site.site_title = "Jambulani"
admin.site.index_title = "Store Management"
