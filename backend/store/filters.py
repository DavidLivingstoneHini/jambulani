import django_filters
from django.db.models import Q
from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    league = django_filters.CharFilter(field_name="league__slug")
    category = django_filters.CharFilter(field_name="category__slug")
    collection = django_filters.CharFilter(field_name="collection__slug")
    is_featured = django_filters.BooleanFilter()
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = Product
        fields = ["league", "category", "collection", "is_featured", "min_price", "max_price", "search"]

    def filter_search(self, queryset, name, value):
        """Search across name, description, league name, and category name"""
        if value:
            return queryset.filter(
                Q(name__icontains=value) |
                Q(description__icontains=value) |
                Q(league__name__icontains=value) |
                Q(category__name__icontains=value)
            ).distinct()
        return queryset
