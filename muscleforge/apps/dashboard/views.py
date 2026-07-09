from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from datetime import timedelta, date
from django.db.models import Sum, Count, Avg
from apps.workout.models import WorkoutSession
from apps.nutrition.models import MealLog, WaterLog
from apps.progress.models import WeightLog
from apps.analytics.models import HabitLog
from apps.accounts.models import UserProfile


def get_dashboard_stats(user, today=None):
    if today is None:
        today = timezone.now().date()

    profile, _ = UserProfile.objects.get_or_create(user=user)

    # Today's nutrition
    today_meals = MealLog.objects.filter(user=user, date=today)
    today_calories = today_meals.aggregate(Sum('calories'))['calories__sum'] or 0
    today_protein = today_meals.aggregate(Sum('protein'))['protein__sum'] or 0
    today_carbs = today_meals.aggregate(Sum('carbs'))['carbs__sum'] or 0
    today_fat = today_meals.aggregate(Sum('fat'))['fat__sum'] or 0

    # Today's water
    today_water = WaterLog.objects.filter(user=user, date=today).aggregate(Sum('amount_ml'))['amount_ml__sum'] or 0
    today_water_liters = round(today_water / 1000, 1)

    # Latest weight
    latest_weight = WeightLog.objects.filter(user=user).first()

    # Workout streak
    streak = calculate_streak(user, today)

    # Weekly workouts
    week_start = today - timedelta(days=today.weekday())
    weekly_sessions = WorkoutSession.objects.filter(
        user=user, date__gte=week_start, is_completed=True
    ).count()

    # Weight chart data (last 30 days)
    weight_logs = WeightLog.objects.filter(
        user=user, date__gte=today - timedelta(days=30)
    ).order_by('date')

    # Calorie chart data (last 7 days)
    calorie_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        cal = MealLog.objects.filter(user=user, date=d).aggregate(Sum('calories'))['calories__sum'] or 0
        calorie_data.append({'date': d.strftime('%a'), 'calories': round(cal)})

    return {
        'profile': profile,
        'today_calories': round(today_calories),
        'today_protein': round(today_protein, 1),
        'today_carbs': round(today_carbs, 1),
        'today_fat': round(today_fat, 1),
        'today_water': today_water_liters,
        'latest_weight': latest_weight.weight if latest_weight else profile.weight,
        'goal_weight': profile.goal_weight,
        'bmi': profile.bmi,
        'bmi_category': profile.bmi_category,
        'streak': streak,
        'weekly_sessions': weekly_sessions,
        'calorie_goal': profile.daily_calorie_goal,
        'protein_goal': profile.daily_protein_goal,
        'water_goal': profile.daily_water_goal,
        'weight_logs': list(weight_logs.values('date', 'weight')),
        'calorie_data': calorie_data,
        'calorie_pct': min(round((today_calories / profile.daily_calorie_goal) * 100), 100) if profile.daily_calorie_goal else 0,
        'protein_pct': min(round((today_protein / profile.daily_protein_goal) * 100), 100) if profile.daily_protein_goal else 0,
        'water_pct': min(round((today_water_liters / profile.daily_water_goal) * 100), 100) if profile.daily_water_goal else 0,
    }


def calculate_streak(user, today):
    streak = 0
    current = today
    while True:
        if WorkoutSession.objects.filter(user=user, date=current, is_completed=True).exists():
            streak += 1
            current -= timedelta(days=1)
        else:
            break
    return streak


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboard/home.html'

    def get(self, request):
        stats = get_dashboard_stats(request.user)
        recent_sessions = WorkoutSession.objects.filter(
            user=request.user
        ).select_related('workout_plan').order_by('-date')[:5]
        return render(request, self.template_name, {**stats, 'recent_sessions': recent_sessions})
