from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Notification, NotificationSettings


@method_decorator(login_required, name='dispatch')
class NotificationListView(View):
    template_name = 'notifications/list.html'

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        unread_count = notifications.filter(is_read=False).count()
        return render(request, self.template_name, {
            'notifications': notifications[:50],
            'unread_count': unread_count,
        })


@login_required
def mark_read(request, pk):
    Notification.objects.filter(pk=pk, user=request.user).update(is_read=True)
    return JsonResponse({'status': 'ok'})


@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notifications:list')


@method_decorator(login_required, name='dispatch')
class NotificationSettingsView(View):
    template_name = 'notifications/settings.html'

    def get(self, request):
        settings_obj, _ = NotificationSettings.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {'settings': settings_obj})

    def post(self, request):
        settings_obj, _ = NotificationSettings.objects.get_or_create(user=request.user)
        settings_obj.workout_reminder = 'workout_reminder' in request.POST
        settings_obj.water_reminder = 'water_reminder' in request.POST
        settings_obj.meal_reminder = 'meal_reminder' in request.POST
        settings_obj.sleep_reminder = 'sleep_reminder' in request.POST
        settings_obj.email_notifications = 'email_notifications' in request.POST
        for field in ['workout_time', 'sleep_time', 'meal_reminder_time']:
            val = request.POST.get(field)
            if val:
                setattr(settings_obj, field, val)
        settings_obj.save()
        from django.contrib import messages
        messages.success(request, 'Notification settings saved!')
        return redirect('notifications:settings')


@login_required
def save_push_subscription(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        settings_obj, _ = NotificationSettings.objects.get_or_create(user=request.user)
        settings_obj.push_subscription = json.dumps(data)
        settings_obj.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def reminder_data(request):
    """Returns reminder times + remaining calories for the service worker."""
    settings_obj, _ = NotificationSettings.objects.get_or_create(user=request.user)
    today = timezone.now().date()

    from apps.nutrition.models import MealLog
    from apps.accounts.models import UserProfile
    logged_calories = MealLog.objects.filter(
        user=request.user, date=today
    ).aggregate(total=Sum('calories'))['total'] or 0

    try:
        goal = request.user.profile.daily_calorie_goal
    except Exception:
        goal = 2000

    remaining = max(0, goal - logged_calories)

    return JsonResponse({
        'workout_reminder': settings_obj.workout_reminder,
        'workout_time': str(settings_obj.workout_time) if settings_obj.workout_time else None,
        'meal_reminder': settings_obj.meal_reminder,
        'meal_reminder_time': str(settings_obj.meal_reminder_time) if settings_obj.meal_reminder_time else None,
        'remaining_calories': remaining,
        'calorie_goal': goal,
    })
