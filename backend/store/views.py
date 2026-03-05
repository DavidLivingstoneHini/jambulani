from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
from django.conf import settings
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Prefetch
from django_filters.rest_framework import DjangoFilterBackend

from accounts.authentication import JWTAuthentication
from config.throttles import (
    AuthEndpointThrottle,
    CartOperationThrottle,
    CheckoutThrottle,
    ProductListThrottle,
    BurstRateThrottle,
    IPBasedThrottle
)
from .models import (
    League, Collection, Category, Patch, Product, ProductImage,
    CartItem, NewsletterSubscriber, SizeChart
)
from .serializers import (
    LeagueSerializer, CollectionSerializer, CategorySerializer, PatchSerializer,
    ProductListSerializer, ProductDetailSerializer, CartItemSerializer,
    NewsletterSubscribeSerializer, SizeChartSerializer
)
from .filters import ProductFilter
from .tasks import send_newsletter_confirmation, cleanup_abandoned_carts, sync_product_stock


class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = League.objects.filter(is_active=True)
    serializer_class = LeagueSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    @method_decorator(cache_page(settings.LEAGUE_CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(settings.LEAGUE_CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Collection.objects.filter(is_active=True)
    serializer_class = CollectionSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    @method_decorator(cache_page(settings.COLLECTION_CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(settings.COLLECTION_CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    @method_decorator(cache_page(settings.CATEGORY_CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Patch.objects.filter(is_active=True)
    serializer_class = PatchSerializer
    permission_classes = [AllowAny]

    @method_decorator(cache_page(settings.CATEGORY_CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Product listing with full filtering, searching, and ordering support.
    Implements aggressive caching for performance.
    """
    lookup_field = 'slug'
    queryset = Product.objects.filter(is_active=True).select_related(
        "league", "category", "collection", "size_chart"
    ).prefetch_related(
        Prefetch("images", queryset=ProductImage.objects.order_by("sort_order")),
        "patches"
    ).only(
        'id', 'name', 'slug', 'price', 'original_price', 'description',
        'is_featured', 'league_id', 'category_id', 'collection_id',
        'size_chart_id', 'stock', 'allow_name_customization',
        'allow_number_customization', 'created_at'
    )
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "league__name", "category__name"]
    ordering_fields = ["price", "created_at", "name"]
    ordering = ["-created_at"]
    throttle_classes = [ProductListThrottle]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    def get_cache_key(self, request):
        """Generate cache key based on query params and page"""
        query_params = frozenset(request.query_params.items())
        return f"product_list_{hash(query_params)}_{request.GET.get('page', 1)}"

    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        # Don't cache authenticated requests
        if request.user.is_authenticated:
            return super().list(request, *args, **kwargs)

        cache_key = self.get_cache_key(request)
        cached_response = cache.get(cache_key)

        if cached_response:
            response = Response(cached_response)
            response['X-Cache'] = 'HIT'
            return response

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=settings.PRODUCT_CACHE_TTL)
        response['X-Cache'] = 'MISS'
        return response

    @method_decorator(cache_page(settings.PRODUCT_CACHE_TTL))
    @method_decorator(vary_on_headers("Authorization"))
    def retrieve(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Don't use cache decorator for authenticated users
            return super().retrieve(request, *args, **kwargs)

        # Use slug for cache key
        lookup_value = kwargs.get(self.lookup_field)
        cache_key = f"product_detail_{lookup_value}"

        cached = cache.get(cache_key)
        if cached:
            response = Response(cached)
            response['X-Cache'] = 'HIT'
            return response

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=settings.PRODUCT_CACHE_TTL)
        response['X-Cache'] = 'MISS'
        return response

    @action(detail=False, methods=["get"], url_path="featured")
    @method_decorator(cache_page(300))  # 5 minutes
    def featured(self, request):
        """Get featured products with caching headers"""
        cache_key = "featured_products"
        cached = cache.get(cache_key)

        if cached:
            response = Response(cached)
            response['X-Cache'] = 'HIT'
            return response

        qs = self.get_queryset().filter(is_featured=True)[:12]
        serializer = ProductListSerializer(
            qs,
            many=True,
            context={"request": request}
        )

        cache.set(cache_key, serializer.data, timeout=300)
        response = Response(serializer.data)
        response['X-Cache'] = 'MISS'
        response['Cache-Control'] = 'max-age=300'
        return response


def _get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


class CartViewSet(viewsets.ViewSet):
    """
    Session-based cart for anonymous users with rate limiting.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    throttle_classes = [CartOperationThrottle]

    def list(self, request):
        session_key = _get_session_key(request)
        cache_key = f"cart_{session_key}"

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        items = CartItem.objects.filter(session_key=session_key).select_related(
            "product", "patch"
        ).prefetch_related("product__images")

        serializer = CartItemSerializer(items, many=True, context={"request": request})
        total = sum(item.subtotal for item in items)

        data = {
            "items": serializer.data,
            "total": str(total),
            "count": items.count()
        }

        cache.set(cache_key, data, timeout=60)  # 1 minute cache
        return Response(data)

    def create(self, request):
        session_key = _get_session_key(request)
        serializer = CartItemSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        existing = CartItem.objects.filter(
            session_key=session_key,
            product=serializer.validated_data["product"],
            size=serializer.validated_data["size"],
            custom_name=serializer.validated_data.get("custom_name", ""),
            custom_number=serializer.validated_data.get("custom_number", ""),
        ).first()

        if existing:
            existing.quantity += serializer.validated_data.get("quantity", 1)
            existing.save()
            # Invalidate cart cache
            cache.delete(f"cart_{session_key}")
            return Response(
                CartItemSerializer(existing, context={"request": request}).data
            )

        item = serializer.save(session_key=session_key)
        # Invalidate cart cache
        cache.delete(f"cart_{session_key}")

        return Response(
            CartItemSerializer(item, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        session_key = _get_session_key(request)
        item = get_object_or_404(CartItem, pk=pk, session_key=session_key)

        quantity = request.data.get("quantity")
        if quantity is not None:
            quantity = int(quantity)
            if quantity <= 0:
                item.delete()
                cache.delete(f"cart_{session_key}")
                return Response(status=status.HTTP_204_NO_CONTENT)
            item.quantity = quantity
            item.save()

        cache.delete(f"cart_{session_key}")
        return Response(
            CartItemSerializer(item, context={"request": request}).data
        )

    def destroy(self, request, pk=None):
        session_key = _get_session_key(request)
        item = get_object_or_404(CartItem, pk=pk, session_key=session_key)
        item.delete()
        cache.delete(f"cart_{session_key}")
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        session_key = _get_session_key(request)
        CartItem.objects.filter(session_key=session_key).delete()
        cache.delete(f"cart_{session_key}")
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewsletterSubscribeView(generics.CreateAPIView):
    serializer_class = NewsletterSubscribeSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AuthEndpointThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscriber = serializer.save()

        # Send confirmation email
        send_newsletter_confirmation.delay(subscriber.email)

        return Response(
            {"message": "Successfully subscribed! Check your email for confirmation."},
            status=status.HTTP_201_CREATED
        )
