from django_filters import rest_framework as filters
from django.db import models
from cars.models import CarProduct, Advertisement


class CarProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_year = filters.NumberFilter(field_name="year", lookup_expr='gte')
    max_year = filters.NumberFilter(field_name="year", lookup_expr='lte')
    min_mileage = filters.NumberFilter(field_name="mileage", lookup_expr='gte')
    max_mileage = filters.NumberFilter(field_name="mileage", lookup_expr='lte')
    
    class Meta:
        model = CarProduct
        fields = ['model', 'body_type', 'color', 'year']


class AdvertisementFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="car_product__price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="car_product__price", lookup_expr='lte')
    min_year = filters.NumberFilter(field_name="car_product__year", lookup_expr='gte')
    max_year = filters.NumberFilter(field_name="car_product__year", lookup_expr='lte')
    min_mileage = filters.NumberFilter(field_name="car_product__mileage", lookup_expr='gte')
    max_mileage = filters.NumberFilter(field_name="car_product__mileage", lookup_expr='lte')
    brand = filters.CharFilter(field_name="car_product__model__brand__brand_name", lookup_expr='icontains')
    model = filters.CharFilter(field_name="car_product__model__model_name", lookup_expr='icontains')
    search = filters.CharFilter(method='search_filter')
    
    class Meta:
        model = Advertisement
        fields = [
            'car_product__model', 'car_product__body_type', 
            'car_product__color', 'car_product__year', 
            'is_active'
        ]
    
    def search_filter(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(car_product__model__brand__brand_name__icontains=value) |
            models.Q(car_product__model__model_name__icontains=value)
        )