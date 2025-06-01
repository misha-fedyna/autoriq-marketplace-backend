from rest_framework import serializers
from users.models import CustomUser, UserProfile, Favorites
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer


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


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    profile = UserProfileSerializer()

    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone', 'password', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = CustomUser.objects.create_user(**validated_data)

        UserProfile.objects.create(
            user=user,
            **profile_data
        )

        return user


class CustomUserSerializer(BaseUserSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ['id', 'email', 'username', 'phone', 'profile', 'is_active']
        read_only_fields = ['is_active']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['id', 'advertisement', 'created_at']
        read_only_fields = ['created_at']
