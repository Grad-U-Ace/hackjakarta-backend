# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import RestaurantViewSet, MenuViewSet, RestaurantMenuViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menus', MenuViewSet)

restaurants_router = routers.NestedSimpleRouter(router, r'restaurants', lookup='restaurant')
restaurants_router.register(r'menus', RestaurantMenuViewSet, basename='restaurant-menus')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(restaurants_router.urls)),
]