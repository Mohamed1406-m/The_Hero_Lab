from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from django.db.models import Sum, Avg, Count
from .models import HabitLog
from .forms import HabitLogForm
from apps.workout.models import WorkoutSession
from apps.nutrition.models import MealLog
from apps.progress.models import WeightLog


@method_decorator(login_required, name='dispatch')
class AnalyticsDashboardView(View):
    template_name = 'analytics/dashboard.html'

    def get(self, request):
        today = timezone.now().date()
        last_30 = today - timedelta(days=30)
        last_7 = today - timedelta(days=7)

        # Habit logs
        habit_logs = HabitLog.objects.filter(user=request.user, date__gte=last_30).order_by('date')

        # Workout analytics
        workout_data = []
        for i in range(29, -1, -1):
            d = today - timedelta(days=i)
            done = WorkoutSession.objects.filter(user=request.user, date=d, is_completed=True).exists()
            workout_data.append({'date': d.strftime('%Y-%m-%d'), 'done': 1 if done else 0})

        # Calorie trend
        calorie_trend = []
        for i in range(29, -1, -1):
            d = today - timedelta(days=i)
            cal = MealLog.objects.filter(user=request.user, date=d).aggregate(Sum('calories'))['calories__sum'] or 0
            calorie_trend.append({'date': d.strftime('%b %d'), 'calories': round(cal)})

        # Weight trend
        weight_trend = list(WeightLog.objects.filter(
            user=request.user, date__gte=last_30
        ).order_by('date').values('date', 'weight'))

        # Sleep & water from habit logs
        sleep_data = [{'date': h.date.strftime('%b %d'), 'hours': h.sleep_hours or 0} for h in habit_logs]
        water_data = [{'date': h.date.strftime('%b %d'), 'liters': h.water_liters or 0} for h in habit_logs]

        # Summary stats
        total_workouts = WorkoutSession.objects.filter(user=request.user, date__gte=last_30, is_completed=True).count()
        avg_sleep = habit_logs.aggregate(Avg('sleep_hours'))['sleep_hours__avg'] or 0
        avg_calories = MealLog.objects.filter(user=request.user, date__gte=last_30).values('date').annotate(
            daily=Sum('calories')).aggregate(Avg('daily'))['daily__avg'] or 0
        
        # Calculate streak
        streak = 0
        current = today
        while WorkoutSession.objects.filter(user=request.user, date=current, is_completed=True).exists():
            streak += 1
            current -= timedelta(days=1)

        return render(request, self.template_name, {
            'workout_data': workout_data,
            'calorie_trend': calorie_trend,
            'weight_trend': weight_trend,
            'sleep_data': sleep_data,
            'water_data': water_data,
            'total_workouts': total_workouts,
            'avg_sleep': round(avg_sleep, 1),
            'avg_calories': round(avg_calories),
            'habit_logs': habit_logs,
            'streak': streak,
        })


@method_decorator(login_required, name='dispatch')
class HabitTrackerView(View):
    template_name = 'analytics/habits.html'

    def get(self, request):
        today = timezone.now().date()
        habit, _ = HabitLog.objects.get_or_create(user=request.user, date=today)
        recent = HabitLog.objects.filter(user=request.user).order_by('-date')[:14]
        form = HabitLogForm(instance=habit)
        return render(request, self.template_name, {'form': form, 'habit': habit, 'recent': recent, 'today': today})

    def post(self, request):
        today = timezone.now().date()
        habit, _ = HabitLog.objects.get_or_create(user=request.user, date=today)
        form = HabitLogForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Habits updated!')
            return redirect('analytics:habits')
        recent = HabitLog.objects.filter(user=request.user).order_by('-date')[:14]
        return render(request, self.template_name, {'form': form, 'habit': habit, 'recent': recent, 'today': today})
