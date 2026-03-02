from rest_framework import serializers
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


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ["id", "name", "slug", "logo", "image"]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "name", "slug", "image"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "league", "collection"]


class PatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patch
        fields = ["id", "name", "image", "extra_price"]


class SizeChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeChart
        fields = ["id", "name", "image", "description"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "is_primary", "sort_order"]


class ProductListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    discount_percentage = serializers.IntegerField(read_only=True)
    league_name = serializers.CharField(source="league.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "original_price",
            "discount_percentage",
            "primary_image",
            "league_name",
            "category_name",
            "is_featured",
        ]

    def get_primary_image(self, obj):
        request = self.context.get("request")
        image = obj.images.filter(is_primary=True).first() or obj.images.first()
        if image and request:
            return request.build_absolute_uri(image.image.url)
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    patches = PatchSerializer(many=True, read_only=True)
    size_chart = SizeChartSerializer(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    league = LeagueSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "original_price",
            "discount_percentage",
            "available_sizes",
            "allow_name_customization",
            "allow_number_customization",
            "images",
            "patches",
            "size_chart",
            "league",
            "category",
            "stock",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True), source="product", write_only=True
    )
    patch = PatchSerializer(read_only=True)
    patch_id = serializers.PrimaryKeyRelatedField(
        queryset=Patch.objects.filter(is_active=True),
        source="patch",
        write_only=True,
        required=False,
        allow_null=True,
    )
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_id",
            "size",
            "custom_name",
            "custom_number",
            "patch",
            "patch_id",
            "quantity",
            "subtotal",
        ]


class NewsletterSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]

    def validate_email(self, value):
        if NewsletterSubscriber.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value
