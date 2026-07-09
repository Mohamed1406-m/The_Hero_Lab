from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
    path('', views.ChallengeListView.as_view(), name='list'),
    path('join/<int:pk>/', views.join_challenge, name='join'),
    path('my/', views.MyChallengesView.as_view(), name='my_challenges'),
    path('achievements/', views.AchievementsView.as_view(), name='achievements'),
]
