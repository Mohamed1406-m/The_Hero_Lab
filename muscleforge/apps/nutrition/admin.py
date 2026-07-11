from django.contrib import admin
from .models import Food, FoodCategory, MealLog, WaterLog, Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'goal_type', 'calories', 'protein', 'carbs', 'fat']
    list_filter = ['goal_type']
    search_fields = ['name']


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'meal_type', 'calories', 'protein', 'carbs', 'fat', 'is_indian', 'is_vegetarian']
    list_filter = ['meal_type', 'is_indian', 'is_vegetarian', 'is_vegan', 'category']
    search_fields = ['name', 'name_hindi']


@admin.register(MealLog)
class MealLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'food', 'meal_type', 'date', 'calories', 'protein']
    list_filter = ['meal_type', 'date']
    search_fields = ['user__email', 'food__name']


@admin.register(WaterLog)
class WaterLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'amount_ml']
    list_filter = ['date']
    search_fields = ['user__email']
