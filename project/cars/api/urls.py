from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdvertisementViewSet, AdvertisementPhotoViewSet

router = DefaultRouter()
router.register(r'advertisements', AdvertisementViewSet)
router.register(r'advertisement-photos', AdvertisementPhotoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]