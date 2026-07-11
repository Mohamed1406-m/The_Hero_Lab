from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='list'),
    path('mark-read/<int:pk>/', views.mark_read, name='mark_read'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('settings/', views.NotificationSettingsView.as_view(), name='settings'),
    path('save-push/', views.save_push_subscription, name='save_push'),
    path('reminder-data/', views.reminder_data, name='reminder_data'),
]
