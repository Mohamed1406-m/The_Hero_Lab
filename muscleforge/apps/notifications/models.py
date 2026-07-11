from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ('workout', 'Workout Reminder'), ('water', 'Water Reminder'),
        ('meal', 'Meal Reminder'), ('sleep', 'Sleep Reminder'),
        ('achievement', 'Achievement'), ('system', 'System'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.title}"


class NotificationSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_settings')
    workout_reminder = models.BooleanField(default=True)
    workout_time = models.TimeField(null=True, blank=True)
    meal_reminder = models.BooleanField(default=True)
    meal_reminder_time = models.TimeField(null=True, blank=True)
    water_reminder = models.BooleanField(default=True)
    sleep_reminder = models.BooleanField(default=True)
    sleep_time = models.TimeField(null=True, blank=True)
    email_notifications = models.BooleanField(default=True)
    push_subscription = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.user.email} Notification Settings"
