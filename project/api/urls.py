from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('users/', include('users.api.urls')),
    path('cars/', include('cars.api.urls')),
]