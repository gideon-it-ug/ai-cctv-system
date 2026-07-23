from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('operator', 'Operator'),
        ('viewer', 'Viewer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Camera(models.Model):
    name = models.CharField(max_length=100, unique=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    EVENT_TYPES = [
        ('person', 'Person Detected'),
        ('motion', 'Motion Detected'),
        ('abandoned_object', 'Abandoned Object'),
        ('license_plate', 'License Plate Detected'),
        ('vehicle', 'Vehicle Detected'),
        ('animal', 'Animal Detected'),
    ]

    camera_name = models.CharField(max_length=100, default="Camera 1")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='person')
    confidence = models.FloatField()
    person_count = models.IntegerField(default=0)
    plate_number = models.CharField(max_length=20, blank=True, null=True)
    detected_class = models.CharField(max_length=50, blank=True, null=True)  # e.g. "car", "dog"
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    notified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.event_type} - {self.camera_name} - {self.timestamp}"