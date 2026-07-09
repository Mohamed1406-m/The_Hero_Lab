from django.contrib import admin
from .models import HabitLog


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'sleep_hours', 'water_liters', 'workout_done', 'mood']
    list_filter = ['date', 'workout_done']
    search_fields = ['user__email']
