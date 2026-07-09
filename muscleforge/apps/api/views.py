from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile
from apps.workout.models import Exercise, WorkoutPlan, WorkoutSession
from apps.nutrition.models import Food, MealLog, WaterLog
from apps.progress.models import WeightLog, BodyMeasurement
from apps.analytics.models import HabitLog
from .serializers import (
    UserSerializer, UserProfileSerializer, ExerciseSerializer,
    WorkoutPlanSerializer, WorkoutSessionSerializer, FoodSerializer,
    MealLogSerializer, WaterLogSerializer, WeightLogSerializer,
    BodyMeasurementSerializer, HabitLogSerializer
)

User = get_user_model()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.filter(is_active=True)
    serializer_class = ExerciseSerializer
    filterset_fields = ['difficulty', 'category', 'equipment']
    search_fields = ['name', 'description']


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filterset_fields = ['plan_type', 'difficulty', 'goal']

    def get_queryset(self):
        return WorkoutPlan.objects.filter(user=self.request.user)


class WorkoutSessionViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSession.objects.all()
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filterset_fields = ['is_completed', 'date']

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)


class FoodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filterset_fields = ['is_vegetarian', 'is_indian', 'meal_type']
    search_fields = ['name', 'name_hindi']


class MealLogViewSet(viewsets.ModelViewSet):
    queryset = MealLog.objects.all()
    serializer_class = MealLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filterset_fields = ['date', 'meal_type']

    def get_queryset(self):
        return MealLog.objects.filter(user=self.request.user)


class WaterLogViewSet(viewsets.ModelViewSet):
    queryset = WaterLog.objects.all()
    serializer_class = WaterLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return WaterLog.objects.filter(user=self.request.user)


class WeightLogViewSet(viewsets.ModelViewSet):
    queryset = WeightLog.objects.all()
    serializer_class = WeightLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return WeightLog.objects.filter(user=self.request.user)


class BodyMeasurementViewSet(viewsets.ModelViewSet):
    queryset = BodyMeasurement.objects.all()
    serializer_class = BodyMeasurementSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return BodyMeasurement.objects.filter(user=self.request.user)


class HabitLogViewSet(viewsets.ModelViewSet):
    queryset = HabitLog.objects.all()
    serializer_class = HabitLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return HabitLog.objects.filter(user=self.request.user)
