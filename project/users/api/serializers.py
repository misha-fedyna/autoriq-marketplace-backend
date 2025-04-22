from rest_framework import serializers
from users.models import CustomUser, UserProfile, Favorites


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'city', 'avatar_url']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone', 'profile', 'is_active']
        read_only_fields = ['is_active']


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for creating user accounts"""
    profile = UserProfileSerializer()
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone', 'password', 'password2', 'profile']
        
    def validate(self, attrs):
        # Check if passwords match
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs
    
    def create(self, validated_data):
        # Extract profile data
        profile_data = validated_data.pop('profile')
        
        # Create the user
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        
        # Create the user profile
        UserProfile.objects.create(
            user=user,
            **profile_data
        )
        
        return user


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['id', 'advertisement', 'created_at']
        read_only_fields = ['created_at']
