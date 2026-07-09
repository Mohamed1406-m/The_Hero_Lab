from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from .models import Notification, NotificationSettings


@method_decorator(login_required, name='dispatch')
class NotificationListView(View):
    template_name = 'notifications/list.html'

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)[:50]
        unread_count = notifications.filter(is_read=False).count()
        return render(request, self.template_name, {
            'notifications': notifications,
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
        workout_time = request.POST.get('workout_time')
        sleep_time = request.POST.get('sleep_time')
        if workout_time:
            settings_obj.workout_time = workout_time
        if sleep_time:
            settings_obj.sleep_time = sleep_time
        settings_obj.save()
        from django.contrib import messages
        messages.success(request, 'Notification settings saved!')
        return redirect('notifications:settings')
