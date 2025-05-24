from rest_framework import serializers
from cars.models import Advertisement, AdvertisementPhoto  # Виправлений імпорт
from users.api.serializers import UserSerializer

class AdvertisementPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementPhoto
        fields = ['id', 'photo', 'order']

# Серіалізатор для короткого відображення оголошення в списку
class AdvertisementListSerializer(serializers.ModelSerializer):
    fuel_type_display = serializers.CharField(source='get_fuel_type_display', read_only=True)
    
    class Meta:
        model = Advertisement
        fields = [
            'id', 'title', 'brand', 'model_name', 'year', 
            'price', 'mileage', 'city', 'main_photo', 
            'fuel_type', 'fuel_type_display', 'engine_capacity',
            'created_at', 'is_active'
        ]

# Серіалізатор для детального відображення оголошення
class AdvertisementDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photos = AdvertisementPhotoSerializer(many=True, read_only=True)
    body_type_display = serializers.CharField(source='get_body_type_display', read_only=True)
    drive_type_display = serializers.CharField(source='get_drive_type_display', read_only=True)
    transmission_display = serializers.CharField(source='get_transmission_display', read_only=True)
    color_display = serializers.CharField(source='get_color_display', read_only=True)
    fuel_type_display = serializers.CharField(source='get_fuel_type_display', read_only=True)
    
    class Meta:
        model = Advertisement
        fields = [
            'id', 'user', 'title', 'description', 'price',
            'brand', 'model_name', 'year', 'body_type', 'body_type_display',
            'drive_type', 'drive_type_display', 'power', 
            'transmission', 'transmission_display', 'color', 'color_display',
            'mileage', 'door_count', 'had_accidents', 'vin_code', 
            'fuel_type', 'fuel_type_display', 'engine_capacity',
            'city', 'main_photo', 'photos',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['created_at', 'updated_at', 'user']

# Серіалізатор для створення нового оголошення
class AdvertisementCreateUpdateSerializer(serializers.ModelSerializer):
    uploaded_photos = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Advertisement
        fields = [
            'title', 'description', 'price',
            'brand', 'model_name', 'year', 'body_type',
            'drive_type', 'power', 'transmission', 'color',
            'mileage', 'door_count', 'had_accidents', 'vin_code', 
            'fuel_type', 'engine_capacity',
            'city', 'main_photo', 'uploaded_photos'
        ]
    
    def create(self, validated_data):
        uploaded_photos = validated_data.pop('uploaded_photos', [])
        
        # Створюємо основне оголошення
        advertisement = Advertisement.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        
        # Зберігаємо додаткові фотографії
        for i, photo in enumerate(uploaded_photos):
            AdvertisementPhoto.objects.create(
                advertisement=advertisement,
                photo=photo,
                order=i+1
            )
        
        return advertisement
    
    def update(self, instance, validated_data):
        uploaded_photos = validated_data.pop('uploaded_photos', [])
        
        # Оновлюємо поля оголошення
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Якщо є нові фотографії, додаємо їх
        if uploaded_photos:
            # Визначаємо наступний порядковий номер
            last_order = instance.photos.order_by('-order').first()
            next_order = 1 if not last_order else last_order.order + 1
            
            for i, photo in enumerate(uploaded_photos):
                AdvertisementPhoto.objects.create(
                    advertisement=instance,
                    photo=photo,
                    order=next_order + i
                )
        
        return instance