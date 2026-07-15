from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import EventViewSet, CameraViewSet, camera_heartbeat, RegisterView, current_user

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'cameras', CameraViewSet)

urlpatterns = router.urls + [
    path('cameras/heartbeat/', camera_heartbeat),
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/me/', current_user),
]