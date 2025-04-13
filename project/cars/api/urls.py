from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BrandViewSet, CarModelViewSet, BodyTypeViewSet, 
    ColorViewSet, CarProductViewSet, AdvertisementViewSet
)

router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'models', CarModelViewSet)
router.register(r'body-types', BodyTypeViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'car-products', CarProductViewSet)
router.register(r'advertisements', AdvertisementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

