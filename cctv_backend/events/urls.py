from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, CameraViewSet, camera_heartbeat

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'cameras', CameraViewSet)

urlpatterns = router.urls + [
    path('cameras/heartbeat/', camera_heartbeat),
]