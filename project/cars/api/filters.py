from django_filters import rest_framework as filters
from django.db import models
from cars.models import Advertisement  # Виправлений імпорт

class AdvertisementFilter(filters.FilterSet):
    """
    Фільтри для пошуку оголошень за різними параметрами.
    """
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_year = filters.NumberFilter(field_name="year", lookup_expr='gte')
    max_year = filters.NumberFilter(field_name="year", lookup_expr='lte')
    min_mileage = filters.NumberFilter(field_name="mileage", lookup_expr='gte')
    max_mileage = filters.NumberFilter(field_name="mileage", lookup_expr='lte')
    min_power = filters.NumberFilter(field_name="power", lookup_expr='gte')
    max_power = filters.NumberFilter(field_name="power", lookup_expr='lte')
    
    # Фільтри за текстовими полями
    brand = filters.CharFilter(field_name="brand", lookup_expr='icontains')
    model = filters.CharFilter(field_name="model_name", lookup_expr='icontains')
    city = filters.CharFilter(field_name="city", lookup_expr='icontains')
    
    # Фільтри за вибірковими полями
    body_type = filters.CharFilter(field_name="body_type")
    drive_type = filters.CharFilter(field_name="drive_type")
    transmission = filters.CharFilter(field_name="transmission")
    color = filters.CharFilter(field_name="color")
    
    # Інші фільтри
    door_count = filters.NumberFilter(field_name="door_count")
    had_accidents = filters.BooleanFilter(field_name="had_accidents")
    
    # Повнотекстовий пошук
    search = filters.CharFilter(method='search_filter')
    
    class Meta:
        model = Advertisement
        fields = [
            'brand', 'model_name', 'year', 'body_type', 'drive_type',
            'transmission', 'color', 'mileage', 'door_count', 
            'had_accidents', 'city', 'is_active'
        ]
    
    def search_filter(self, queryset, name, value):
        """
        Повнотекстовий пошук по основним полям
        """
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(brand__icontains=value) |
            models.Q(model_name__icontains=value) |
            models.Q(city__icontains=value)
        )