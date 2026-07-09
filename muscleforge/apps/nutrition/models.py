from django.db import models
from django.conf import settings


class FoodCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'Food Categories'

    def __str__(self):
        return self.name


class Food(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'), ('lunch', 'Lunch'),
        ('dinner', 'Dinner'), ('snack', 'Snack'), ('any', 'Any'),
    ]

    name = models.CharField(max_length=100)
    name_hindi = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True, blank=True)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, default='any')
    serving_size = models.FloatField(default=100, help_text='Grams')
    serving_unit = models.CharField(max_length=20, default='g')
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    fiber = models.FloatField(default=0)
    sugar = models.FloatField(default=0)
    sodium = models.FloatField(default=0)
    is_indian = models.BooleanField(default=True)
    is_vegetarian = models.BooleanField(default=True)
    is_vegan = models.BooleanField(default=False)
    image = models.ImageField(upload_to='foods/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def macros_per_serving(self, quantity_g):
        ratio = quantity_g / self.serving_size
        return {
            'calories': round(self.calories * ratio, 1),
            'protein': round(self.protein * ratio, 1),
            'carbs': round(self.carbs * ratio, 1),
            'fat': round(self.fat * ratio, 1),
        }


class MealLog(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'), ('lunch', 'Lunch'),
        ('dinner', 'Dinner'), ('snack', 'Snack'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meal_logs')
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField(default=100, help_text='Grams')
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'meal_type']

    def save(self, *args, **kwargs):
        macros = self.food.macros_per_serving(self.quantity)
        self.calories = macros['calories']
        self.protein = macros['protein']
        self.carbs = macros['carbs']
        self.fat = macros['fat']
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.food.name} ({self.date})"


class WaterLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='water_logs')
    date = models.DateField()
    amount_ml = models.PositiveIntegerField(default=250)
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return f"{self.user.email} - {self.amount_ml}ml ({self.date})"
