from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import models
from cars.models import Brand, CarModel, BodyType, Color, CarProduct, Advertisement
from .serializers import (
    BrandSerializer, CarModelSerializer, BodyTypeSerializer,
    ColorSerializer, CarProductSerializer, CarProductDetailSerializer,
    AdvertisementSerializer, AdvertisementCreateSerializer
)
from .filters import CarProductFilter, AdvertisementFilter
from users.api.permissions import IsOwnerOrReadOnly
from users.models import Favorites


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['brand_name']
    ordering_fields = ['brand_name']


class CarModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand']
    search_fields = ['model_name']


class BodyTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BodyType.objects.all()
    serializer_class = BodyTypeSerializer
    permission_classes = [permissions.AllowAny]


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.AllowAny]


class CarProductViewSet(viewsets.ModelViewSet):
    queryset = CarProduct.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CarProductFilter
    ordering_fields = ['price', 'year', 'mileage']
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return CarProductDetailSerializer
        return CarProductSerializer


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.filter(is_active=True, deleted_at=None)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AdvertisementFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'car_product__price']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AdvertisementCreateSerializer
        return AdvertisementSerializer
    
    def get_queryset(self):
        # For listing, only show active ads
        if self.action == 'list':
            return Advertisement.objects.filter(is_active=True, deleted_at=None)
        
        # For other actions, users should be able to see their own inactive/deleted ads
        user = self.request.user
        if user.is_authenticated:
            return Advertisement.objects.filter(
                models.Q(is_active=True, deleted_at=None) | 
                models.Q(user=user)
            )
        
        return Advertisement.objects.filter(is_active=True, deleted_at=None)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        advertisement = self.get_object()
        favorite, created = Favorites.objects.get_or_create(
            user=request.user,
            advertisement=advertisement
        )
        
        if not created:
            favorite.delete()
            return Response({"status": "removed from favorites"})
            
        return Response({"status": "added to favorites"})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        advertisement = self.get_object()
        advertisement.is_active = False
        advertisement.save()
        return Response({"status": "advertisement deactivated"})
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        advertisement = self.get_object()
        advertisement.is_active = True
        advertisement.save()
        return Response({"status": "advertisement activated"})
    
    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        advertisement = self.get_object()
        advertisement.deleted_at = timezone.now()
        advertisement.is_active = False
        advertisement.save()
        return Response({"status": "advertisement deleted"})