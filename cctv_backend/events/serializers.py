from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import Event, Camera


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