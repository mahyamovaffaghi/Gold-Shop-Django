import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method='filter_by_category', label='Category')
    subcategory = django_filters.CharFilter(method='filter_by_subcategory', label='Subcategory')
    brand = django_filters.CharFilter(method='filter_by_brand', label='Brand')

    class Meta:
        model = Product
        fields = []

    def filter_by_category(self, queryset, name, value):
        return queryset.filter(
            category__name=value,
            category__is_brand=False,
            category__sub_category_accessory=False
        )

    def filter_by_subcategory(self, queryset, name, value):
        return queryset.filter(
            category__name=value,
            category__sub_category_accessory=True
        )

    def filter_by_brand(self, queryset, name, value):
        return queryset.filter(
            category__name=value,
            category__is_brand=True
        )

