from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from .models import Food, FoodCategory, MealLog, WaterLog
from .forms import MealLogForm, WaterLogForm


@method_decorator(login_required, name='dispatch')
class NutritionDashboardView(View):
    template_name = 'nutrition/dashboard.html'

    def get(self, request):
        today = timezone.now().date()
        meal_logs = MealLog.objects.filter(user=request.user, date=today).select_related('food')
        water_logs = WaterLog.objects.filter(user=request.user, date=today)

        totals = meal_logs.aggregate(
            total_calories=Sum('calories'), total_protein=Sum('protein'),
            total_carbs=Sum('carbs'), total_fat=Sum('fat')
        )
        total_water = water_logs.aggregate(Sum('amount_ml'))['amount_ml__sum'] or 0

        meals_by_type = {}
        for meal_type, _ in MealLog.MEAL_TYPE_CHOICES:
            meals_by_type[meal_type] = meal_logs.filter(meal_type=meal_type)

        # Get foods for dropdown
        foods = Food.objects.all()[:10]

        return render(request, self.template_name, {
            'meal_logs': meal_logs,
            'meals_by_type': meals_by_type,
            'water_logs': water_logs,
            'totals': totals,
            'total_water_ml': total_water,
            'total_water_liters': round(total_water / 1000, 1),
            'today': today,
            'meal_form': MealLogForm(),
            'water_form': WaterLogForm(),
            'foods': foods,
            'user_profile': request.user.profile,
        })


@method_decorator(login_required, name='dispatch')
class FoodSearchView(View):
    template_name = 'nutrition/food_search.html'

    def get(self, request):
        query = request.GET.get('q', '')
        category = request.GET.get('category')
        is_vegetarian = request.GET.get('vegetarian')
        foods = Food.objects.all()

        if query:
            foods = foods.filter(name__icontains=query)
        if category:
            foods = foods.filter(category__name=category)
        if is_vegetarian:
            foods = foods.filter(is_vegetarian=True)

        categories = FoodCategory.objects.all()
        return render(request, self.template_name, {
            'foods': foods[:50], 'query': query, 'categories': categories
        })


@login_required
def add_meal(request):
    if request.method == 'POST':
        form = MealLogForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, f'{meal.food.name} added to {meal.get_meal_type_display()}!')
        return redirect('nutrition:dashboard')
    return redirect('nutrition:dashboard')


@login_required
def delete_meal(request, pk):
    from django.shortcuts import get_object_or_404
    meal = get_object_or_404(MealLog, pk=pk, user=request.user)
    meal.delete()
    return JsonResponse({'status': 'ok'})


@login_required
def add_water(request):
    if request.method == 'POST':
        form = WaterLogForm(request.POST)
        if form.is_valid():
            water = form.save(commit=False)
            water.user = request.user
            water.save()
            messages.success(request, f'{water.amount_ml}ml water logged!')
    return redirect('nutrition:dashboard')


@method_decorator(login_required, name='dispatch')
class MealHistoryView(View):
    template_name = 'nutrition/history.html'

    def get(self, request):
        from datetime import timedelta
        today = timezone.now().date()
        logs = MealLog.objects.filter(
            user=request.user,
            date__gte=today - timedelta(days=30)
        ).select_related('food').order_by('-date', 'meal_type')
        return render(request, self.template_name, {'logs': logs})
