from django.db import models
from django.conf import settings


class WeightLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weight_logs')
    date = models.DateField()
    weight = models.FloatField(help_text='Weight in kg')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.email} - {self.weight}kg ({self.date})"


class BodyMeasurement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='measurements')
    date = models.DateField()
    chest = models.FloatField(null=True, blank=True, help_text='cm')
    waist = models.FloatField(null=True, blank=True, help_text='cm')
    hips = models.FloatField(null=True, blank=True, help_text='cm')
    arms = models.FloatField(null=True, blank=True, help_text='cm')
    thighs = models.FloatField(null=True, blank=True, help_text='cm')
    calves = models.FloatField(null=True, blank=True, help_text='cm')
    shoulders = models.FloatField(null=True, blank=True, help_text='cm')
    neck = models.FloatField(null=True, blank=True, help_text='cm')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.email} - Measurements ({self.date})"


class ProgressPhoto(models.Model):
    ANGLE_CHOICES = [('front', 'Front'), ('back', 'Back'), ('side', 'Side')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress_photos')
    date = models.DateField()
    photo = models.ImageField(upload_to='progress_photos/')
    angle = models.CharField(max_length=10, choices=ANGLE_CHOICES, default='front')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.email} - {self.angle} ({self.date})"
