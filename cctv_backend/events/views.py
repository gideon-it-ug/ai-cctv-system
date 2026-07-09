from rest_framework import viewsets
from .models import Event, Camera
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CameraSerializer, EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


@api_view(['POST'])
def camera_heartbeat(request):
    name = request.data.get('camera_name', 'Camera 1')
    camera, _ = Camera.objects.get_or_create(name=name)
    camera.save()  # bumps last_seen via auto_now
    return Response({'status': 'ok', 'camera': name})