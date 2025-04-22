from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, CarModel, BodyType, Color, CarProduct, Advertisement

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'brand']
    list_filter = ['brand']
    search_fields = ['model_name', 'brand__brand_name']

class CarProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'model', 'body_type', 'year', 'price', 'color', 'mileage']
    list_filter = ['model__brand', 'body_type', 'year', 'color']
    search_fields = ['model__model_name', 'model__brand__brand_name']
    
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'get_car_info', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'car_product__model__brand']
    search_fields = ['title', 'description', 'user__email', 'car_product__model__model_name']
    readonly_fields = ['created_at', 'updated_at']
    
    # Для форматування інформації про автомобіль
    def get_car_info(self, obj):
        if obj.car_product:
            return format_html(
                '{} - {} | {}₴ | {} км',
                obj.car_product.model,
                obj.car_product.year,
                obj.car_product.price,
                obj.car_product.mileage
            )
        return '-'
    get_car_info.short_description = 'Автомобіль'
    
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

class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'founded_year']
    search_fields = ['brand_name']

class BodyTypeAdmin(admin.ModelAdmin):
    list_display = ['body_type_name']

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_display', 'hex_code']
    
    # Красиве відображення кольору
    def color_display(self, obj):
        return format_html(
            '<div style="width:20px;height:20px;background-color:{};border:1px solid #ddd;"></div>',
            obj.hex_code
        )
    color_display.short_description = 'Відображення'

# Реєстрація моделей в адмін-панелі
admin.site.register(Brand, BrandAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(BodyType, BodyTypeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(CarProduct, CarProductAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)