from rest_framework import serializers
from .models import Restaurant, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'menu_name', 'price', 'description', 'buy_count']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant_name', 'category', 'distance', 'rating', 'avatar']


class MenuWithRestaurantSerializer(MenuSerializer):
    restaurant = RestaurantSerializer(read_only=True)

    class Meta(MenuSerializer.Meta):
        fields = MenuSerializer.Meta.fields + ['restaurant']


class RestaurantWithMenusSerializer(RestaurantSerializer):
    menus = MenuSerializer(many=True, read_only=True)

    class Meta(RestaurantSerializer.Meta):
        fields = RestaurantSerializer.Meta.fields + ['menus']
