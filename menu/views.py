from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer, MenuWithRestaurantSerializer, RestaurantWithMenusSerializer
from .filters import RestaurantFilter, MenuFilter


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RestaurantFilter
    ordering_fields = ['restaurant_name', 'rating', 'distance']
    ordering = ['restaurant_name']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RestaurantWithMenusSerializer
        return RestaurantSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MenuFilter
    ordering_fields = ['menu_name', 'price', 'buy_count', 'restaurant__restaurant_name']
    ordering = ['menu_name']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return MenuWithRestaurantSerializer
        return MenuSerializer

class RestaurantMenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MenuFilter
    ordering_fields = ['menu_name', 'price', 'buy_count', 'restaurant__restaurant_name', 'restaurant__distance']
    ordering = ['menu_name']

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_pk')
        return Menu.objects.filter(restaurant_id=restaurant_id)