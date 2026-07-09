from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile
from apps.workout.models import Exercise, WorkoutPlan, WorkoutSession
from apps.nutrition.models import Food, MealLog, WaterLog
from apps.progress.models import WeightLog, BodyMeasurement
from apps.analytics.models import HabitLog

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'full_name', 'avatar_url']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'slug', 'description', 'difficulty', 'category', 'equipment', 'calories_per_minute']


class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = ['id', 'name', 'description', 'plan_type', 'difficulty', 'goal', 'is_ai_generated']


class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = ['id', 'name', 'date', 'duration_minutes', 'calories_burned', 'is_completed']


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'calories', 'protein', 'carbs', 'fat', 'is_vegetarian', 'is_indian']


class MealLogSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)

    class Meta:
        model = MealLog
        fields = ['id', 'date', 'meal_type', 'food', 'quantity', 'calories', 'protein']


class WaterLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterLog
        fields = ['id', 'date', 'amount_ml']


class WeightLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightLog
        fields = ['id', 'date', 'weight', 'notes']


class BodyMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyMeasurement
        fields = ['id', 'date', 'chest', 'waist', 'arms', 'thighs', 'calves']


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = '__all__'
