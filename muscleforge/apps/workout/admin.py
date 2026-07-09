from django.contrib import admin
from .models import Exercise, MuscleGroup, WorkoutPlan, WorkoutDay, WorkoutExercise, WorkoutSession


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'difficulty', 'category', 'equipment', 'calories_per_minute', 'is_active']
    list_filter = ['difficulty', 'category', 'equipment', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['muscles_worked']


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'plan_type', 'difficulty', 'goal', 'is_ai_generated', 'is_public']
    list_filter = ['plan_type', 'difficulty', 'goal', 'is_ai_generated']
    search_fields = ['name', 'user__email']


@admin.register(WorkoutDay)
class WorkoutDayAdmin(admin.ModelAdmin):
    list_display = ['plan', 'day_number', 'name', 'focus']


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'duration_minutes', 'calories_burned', 'is_completed']
    list_filter = ['is_completed', 'date']
    search_fields = ['user__email']
