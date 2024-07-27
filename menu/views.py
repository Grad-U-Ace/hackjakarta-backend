from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from menu.models import Restaurant, Menu
from menu.serializers import RestaurantSerializer, MenuSerializer


# Create your views here.
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_pk')
        if restaurant_id:
            return Menu.objects.filter(restaurant_id=restaurant_id)
        return super().get_queryset()


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
