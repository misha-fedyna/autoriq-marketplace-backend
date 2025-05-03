from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'profile', UserViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
    path('', include(router.urls)),
]