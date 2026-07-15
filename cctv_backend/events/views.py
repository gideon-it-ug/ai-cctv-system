from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Event, Camera
from .serializers import EventSerializer, CameraSerializer, RegisterSerializer, UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # detector script posts without login; lock down later for production

    def get_serializer_context(self):
        return {'request': self.request}


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [AllowAny]


@api_view(['POST'])
@permission_classes([AllowAny])
def camera_heartbeat(request):
    name = request.data.get('camera_name', 'Camera 1')
    camera, _ = Camera.objects.get_or_create(name=name)
    camera.save()
    return Response({'status': 'ok', 'camera': name})


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)