from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationView, UserViewSet, FavoriteViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]