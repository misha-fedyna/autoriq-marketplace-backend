from rest_framework import serializers
from cars.models import Brand, CarModel, BodyType, Color, CarProduct, Advertisement
from users.api.serializers import UserSerializer


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'brand_name', 'description', 'founded_year']


class CarModelSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        source='brand',
        write_only=True
    )
    
    class Meta:
        model = CarModel
        fields = ['id', 'model_name', 'brand', 'brand_id']


class BodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyType
        fields = ['id', 'body_type_name']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


class CarProductSerializer(serializers.ModelSerializer):
    model = serializers.StringRelatedField(read_only=True)
    body_type = serializers.StringRelatedField(read_only=True)
    color = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = CarProduct
        fields = [
            'id', 'model', 'body_type', 'year', 
            'price', 'color', 'mileage', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CarProductDetailSerializer(serializers.ModelSerializer):
    model = CarModelSerializer(read_only=True)
    model_id = serializers.PrimaryKeyRelatedField(
        queryset=CarModel.objects.all(),
        source='model',
        write_only=True
    )
    body_type = BodyTypeSerializer(read_only=True)
    body_type_id = serializers.PrimaryKeyRelatedField(
        queryset=BodyType.objects.all(),
        source='body_type',
        write_only=True
    )
    color = ColorSerializer(read_only=True)
    color_id = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(),
        source='color',
        required=False,
        allow_null=True,
        write_only=True
    )
    
    class Meta:
        model = CarProduct
        fields = [
            'id', 'model', 'model_id', 'body_type', 'body_type_id',
            'year', 'price', 'color', 'color_id', 'mileage',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AdvertisementSerializer(serializers.ModelSerializer):
    car_product = CarProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Advertisement
        fields = [
            'id', 'title', 'description', 'car_product', 
            'user', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['created_at', 'updated_at', 'user']


class AdvertisementCreateSerializer(serializers.ModelSerializer):
    car_product = CarProductDetailSerializer()
    brand_id = serializers.IntegerField(write_only=True)  # Для вибору бренду
    
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'car_product', 'brand_id']
    
    def create(self, validated_data):
        brand_id = validated_data.pop('brand_id', None)
        car_product_data = validated_data.pop('car_product')
        
        # Create the car product
        car_product = CarProduct.objects.create(**car_product_data)
        
        # Create the advertisement with active status
        advertisement = Advertisement.objects.create(
            car_product=car_product,
            user=self.context['request'].user,
            is_active=True,  # Активувати одразу
            **validated_data
        )
        
        return advertisement