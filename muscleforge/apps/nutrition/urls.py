from django.urls import path
from . import views

app_name = 'nutrition'

urlpatterns = [
    path('', views.NutritionDashboardView.as_view(), name='dashboard'),
    path('search/', views.FoodSearchView.as_view(), name='food_search'),
    path('add-meal/', views.add_meal, name='add_meal'),
    path('delete-meal/<int:pk>/', views.delete_meal, name='delete_meal'),
    path('add-water/', views.add_water, name='add_water'),
    path('history/', views.MealHistoryView.as_view(), name='history'),
    path('recipes/', views.RecipeListView.as_view(), name='recipes'),
]
