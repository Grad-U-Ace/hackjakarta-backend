from rest_framework import serializers

from menu.models import Menu, Restaurant


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'menu_name', 'restaurant', 'price', 'description', 'buy_count']


class RestaurantSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant_name', 'category', 'distance', 'rating', 'avatar', 'menus']


