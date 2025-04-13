from rest_framework import serializers
from reviews.models import Review
from users.api.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'car_product', 'content', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        # Prevent duplicate reviews
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Only check on create, not update
            if not self.instance:
                user = request.user
                car_product = attrs.get('car_product')
                if Review.objects.filter(user=user, car_product=car_product).exists():
                    raise serializers.ValidationError(
                        {"detail": "You have already reviewed this car."}
                    )
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)