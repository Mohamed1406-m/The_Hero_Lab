from django.urls import path
from . import views

app_name = 'ai_coach'

urlpatterns = [
    path('', views.AIChatView.as_view(), name='chat'),
    path('stream/', views.stream_chat, name='stream'),
    path('new-session/', views.new_session, name='new_session'),
    path('delete-session/<int:session_id>/', views.delete_session, name='delete_session'),
    path('diet-plan/', views.DietPlanView.as_view(), name='diet_plan'),
    path('report/', views.AIReportView.as_view(), name='report'),
    path('delete-report/<int:report_id>/', views.delete_report, name='delete_report'),
]
