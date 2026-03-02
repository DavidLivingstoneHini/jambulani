from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from accounts.authentication import JWTAuthentication
from .models import League, Collection, Category, Patch, Product, CartItem, NewsletterSubscriber
from .serializers import (
    LeagueSerializer, CollectionSerializer, CategorySerializer, PatchSerializer,
    ProductListSerializer, ProductDetailSerializer, CartItemSerializer,
    NewsletterSubscribeSerializer,
)
from .filters import ProductFilter


class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = League.objects.filter(is_active=True)
    serializer_class = LeagueSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Collection.objects.filter(is_active=True)
    serializer_class = CollectionSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class PatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Patch.objects.filter(is_active=True)
    serializer_class = PatchSerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related(
        "league", "category", "collection", "size_chart"
    ).prefetch_related("images", "patches")
    filterset_class = ProductFilter
    permission_classes = [AllowAny]
    search_fields = ["name", "description", "league__name", "category__name"]
    ordering_fields = ["price", "created_at", "name"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    def get_object(self):
        queryset = self.get_queryset()
        lookup_value = self.kwargs[self.lookup_field]
        obj = get_object_or_404(queryset, pk=lookup_value) if lookup_value.isdigit() \
            else get_object_or_404(queryset, slug=lookup_value)
        return obj

    @action(detail=False, methods=["get"])
    def featured(self, request):
        qs = self.get_queryset().filter(is_featured=True)[:8]
        serializer = ProductListSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)


def _get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


class CartViewSet(viewsets.ViewSet):
    """
    Session-based cart for anonymous users.
    When authenticated, the session key is still used but tied to the request.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def list(self, request):
        session_key = _get_session_key(request)
        items = CartItem.objects.filter(session_key=session_key).select_related(
            "product", "patch"
        ).prefetch_related("product__images")
        serializer = CartItemSerializer(items, many=True, context={"request": request})
        total = sum(item.subtotal for item in items)
        return Response({"items": serializer.data, "total": str(total), "count": items.count()})

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
            return Response(CartItemSerializer(existing, context={"request": request}).data)
        item = serializer.save(session_key=session_key)
        return Response(
            CartItemSerializer(item, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        session_key = _get_session_key(request)
        item = get_object_or_404(CartItem, pk=pk, session_key=session_key)
        return Response(CartItemSerializer(item, context={"request": request}).data)

    def partial_update(self, request, pk=None):
        session_key = _get_session_key(request)
        item = get_object_or_404(CartItem, pk=pk, session_key=session_key)
        quantity = request.data.get("quantity")
        if quantity is not None:
            quantity = int(quantity)
            if quantity <= 0:
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            item.quantity = quantity
            item.save()
        return Response(CartItemSerializer(item, context={"request": request}).data)

    def destroy(self, request, pk=None):
        session_key = _get_session_key(request)
        item = get_object_or_404(CartItem, pk=pk, session_key=session_key)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        session_key = _get_session_key(request)
        CartItem.objects.filter(session_key=session_key).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewsletterSubscribeView(generics.CreateAPIView):
    serializer_class = NewsletterSubscribeSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Successfully subscribed!"}, status=status.HTTP_201_CREATED)
