from django.contrib import admin
from .models import WeightLog, BodyMeasurement, ProgressPhoto


@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight', 'date']
    list_filter = ['date']
    search_fields = ['user__email']


@admin.register(BodyMeasurement)
class BodyMeasurementAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'chest', 'waist', 'arms']
    search_fields = ['user__email']


@admin.register(ProgressPhoto)
class ProgressPhotoAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'angle']
    list_filter = ['angle']
    search_fields = ['user__email']
