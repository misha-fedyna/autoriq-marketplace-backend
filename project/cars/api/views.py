from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import models
from cars.models import Advertisement, AdvertisementPhoto
from .serializers import (
    AdvertisementListSerializer,
    AdvertisementDetailSerializer,
    AdvertisementCreateUpdateSerializer,
    AdvertisementPhotoSerializer
)
from .filters import AdvertisementFilter
from users.api.permissions import IsOwnerOrReadOnly
from users.models import Favorites
from rest_framework.parsers import MultiPartParser, FormParser


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.filter(is_active=True, deleted_at=None)
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AdvertisementFilter
    search_fields = ['title', 'description', 'model_name', 'brand', 'city']
    ordering_fields = ['created_at', 'price', 'year', 'mileage']
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AdvertisementCreateUpdateSerializer
        elif self.action == 'retrieve':
            return AdvertisementDetailSerializer
        return AdvertisementListSerializer

    def get_queryset(self):
        # Для публічного списку, показуємо тільки активні оголошення
        if self.action == 'list':
            return Advertisement.objects.filter(is_active=True, deleted_at=None)

        # Для власника, показуємо всі його оголошення (включаючи неактивні)
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


class AdvertisementPhotoViewSet(viewsets.ModelViewSet):
    queryset = AdvertisementPhoto.objects.all()
    serializer_class = AdvertisementPhotoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return AdvertisementPhoto.objects.filter(advertisement__user=self.request.user)

    def perform_create(self, serializer):
        advertisement_id = self.request.data.get('advertisement')
        advertisement = Advertisement.objects.get(id=advertisement_id)

        if advertisement.user != self.request.user:
            raise permissions.PermissionDenied(
                "You don't have permission to add photos to this advertisement.")

        # Визначаємо наступний порядковий номер
        order = AdvertisementPhoto.objects.filter(
            advertisement=advertisement).count() + 1

        serializer.save(advertisement=advertisement, order=order)

    @action(detail=True, methods=['post'])
    def change_order(self, request, pk=None):
        photo = self.get_object()
        new_order = request.data.get('order')

        if new_order is None:
            return Response({"error": "Order parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_order = int(new_order)
        except ValueError:
            return Response({"error": "Order must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        photo.order = new_order
        photo.save()

        return Response({"status": "order updated"})
