# filters.py
import django_filters
from .models import Restaurant, Menu


class RestaurantFilter(django_filters.FilterSet):
    min_rating = django_filters.NumberFilter(field_name="rating", lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name="rating", lookup_expr='lte')
    max_distance = django_filters.NumberFilter(field_name="distance", lookup_expr='lte')

    class Meta:
        model = Restaurant
        fields = ['category', 'min_rating', 'max_rating', 'max_distance']


class MenuFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_buy_count = django_filters.NumberFilter(field_name="buy_count", lookup_expr='gte')
    menu_name = django_filters.CharFilter(field_name="menu_name", lookup_expr='icontains')
    restaurant_name = django_filters.CharFilter(field_name="restaurant__restaurant_name", lookup_expr='icontains', )
    restaurant_category = django_filters.CharFilter(field_name="restaurant__category", lookup_expr='icontains')
    restaurant_max_distance = django_filters.NumberFilter(field_name="restaurant__distance", lookup_expr='lte')
    restaurant_min_rating = django_filters.NumberFilter(field_name="restaurant__rating", lookup_expr='gte')

    class Meta:
        model = Menu
        fields = ['restaurant', 'min_price', 'max_price', 'min_buy_count', 'menu_name', 'restaurant_name', 'restaurant_category', 'restaurant_max_distance', 'restaurant_min_rating']
