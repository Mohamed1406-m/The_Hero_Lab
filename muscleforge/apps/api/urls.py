from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'profiles', views.UserProfileViewSet, basename='profile')
router.register(r'exercises', views.ExerciseViewSet, basename='exercise')
router.register(r'workout-plans', views.WorkoutPlanViewSet, basename='workout-plan')
router.register(r'workout-sessions', views.WorkoutSessionViewSet, basename='workout-session')
router.register(r'foods', views.FoodViewSet, basename='food')
router.register(r'meal-logs', views.MealLogViewSet, basename='meal-log')
router.register(r'water-logs', views.WaterLogViewSet, basename='water-log')
router.register(r'weight-logs', views.WeightLogViewSet, basename='weight-log')
router.register(r'measurements', views.BodyMeasurementViewSet, basename='measurement')
router.register(r'habit-logs', views.HabitLogViewSet, basename='habit-log')

urlpatterns = [
    path('', include(router.urls)),
]
