from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Event, Camera, Profile


class EventSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class CameraSerializer(serializers.ModelSerializer):
    online = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = ['id', 'name', 'last_seen', 'online']

    def get_online(self, obj):
        return timezone.now() - obj.last_seen < timedelta(seconds=15)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        Profile.objects.create(user=user, role='viewer')
        return user


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else 'viewer'