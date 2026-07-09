from django.contrib.auth.context_processors import PermWrapper
from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'notification_count': unread_count}
    return {}
