import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    league = django_filters.CharFilter(field_name="league__slug")
    category = django_filters.CharFilter(field_name="category__slug")
    collection = django_filters.CharFilter(field_name="collection__slug")
    is_featured = django_filters.BooleanFilter()

    class Meta:
        model = Product
        fields = ["league", "category", "collection", "is_featured", "min_price", "max_price"]
