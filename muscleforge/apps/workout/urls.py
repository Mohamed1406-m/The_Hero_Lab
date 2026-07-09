from django.urls import path
from . import views

app_name = 'workout'

urlpatterns = [
    path('exercises/', views.ExerciseListView.as_view(), name='exercises'),
    path('exercises/<slug:slug>/', views.ExerciseDetailView.as_view(), name='exercise_detail'),
    path('plans/', views.WorkoutPlanListView.as_view(), name='plans'),
    path('plans/<int:pk>/', views.WorkoutPlanDetailView.as_view(), name='plan_detail'),
    path('plans/generate/', views.GenerateWorkoutPlanView.as_view(), name='generate_plan'),
    path('sessions/', views.WorkoutSessionView.as_view(), name='sessions'),
    path('sessions/<int:pk>/complete/', views.complete_session, name='complete_session'),
]
