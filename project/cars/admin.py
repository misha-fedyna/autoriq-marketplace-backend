from django.contrib import admin
from django.utils.html import format_html
from .models import Advertisement, AdvertisementPhoto

class AdvertisementPhotoInline(admin.TabularInline):
    model = AdvertisementPhoto
    extra = 1
    fields = ['photo', 'order']
    readonly_fields = ['photo_preview']
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" />', obj.photo.url)
        return '-'
    photo_preview.short_description = 'Перегляд'

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'car_info', 'engine_info', 'city', 'created_at', 'is_active']
    list_filter = [
        'is_active', 'created_at', 'brand', 'body_type', 
        'transmission', 'color', 'had_accidents', 'fuel_type'
    ]
    search_fields = [
        'title', 'description', 'user__email', 
        'brand', 'model_name', 'city', 'vin_code'
    ]
    readonly_fields = ['created_at', 'updated_at', 'photo_preview']
    inlines = [AdvertisementPhotoInline]
    
    fieldsets = (
        ('Основна інформація', {
            'fields': ('user', 'title', 'description', 'price', 'city', 'main_photo', 'photo_preview')
        }),
        ('Інформація про автомобіль', {
            'fields': ('brand', 'model_name', 'year', 'body_type')
        }),
        ('Двигун і характеристики', {
            'fields': ('power', 'fuel_type', 'engine_capacity', 'drive_type')
        }),
        ('Додаткові характеристики', {
            'fields': ('transmission', 'color', 'mileage', 'door_count', 'had_accidents', 'vin_code')
        }),
        ('Статус', {
            'fields': ('is_active', 'deleted_at', 'created_at', 'updated_at')
        }),
    )
    
    # Для форматування інформації про автомобіль
    def car_info(self, obj):
        return format_html(
            '{} {} - {} | {}₴',
            obj.brand,
            obj.model_name,
            obj.year,
            obj.price
        )
    car_info.short_description = 'Автомобіль'
    
    # Для форматування інформації про двигун і пробіг
    def engine_info(self, obj):
        fuel_type = obj.get_fuel_type_display()
        return format_html(
            '{} {}л | {} | {} км',
            fuel_type,
            obj.engine_capacity,
            obj.get_transmission_display(),
            obj.mileage
        )
    engine_info.short_description = 'Двигун і пробіг'
    
    def photo_preview(self, obj):
        if obj.main_photo:
            return format_html('<img src="{}" width="300" />', obj.main_photo.url)
        return 'Немає фото'
    photo_preview.short_description = 'Фото'
    
    # Автоматичне встановлення користувача при створенні
    def save_model(self, request, obj, form, change):
        if not obj.user_id:  # Якщо користувач не встановлений
            obj.user = request.user
        super().save_model(request, obj, form, change)
    
    # При редагуванні користувач бачитиме лише свої оголошення (якщо він не адмін)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

admin.site.register(Advertisement, AdvertisementAdmin)