from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from menu.filters import RestaurantFilter, MenuFilter
from menu.models import Restaurant, Menu
from menu.serializers import RestaurantSerializer, MenuSerializer


# Create your views here.
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category', 'rating']
    ordering_fields = ['restaurant_name', 'rating', 'distance']
    ordering = ['restaurant_name']  # default ordering
    filterset_class = RestaurantFilter


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MenuFilter
    ordering_fields = ['menu_name', 'price', 'buy_count', 'restaurant__restaurant_name', 'restaurant__distance']
    ordering = ['menu_name']

class RestaurantMenuViewSet(MenuViewSet):
    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_pk')
        return Menu.objects.filter(restaurant_id=restaurant_id)
