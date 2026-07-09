from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.ProgressDashboardView.as_view(), name='dashboard'),
    path('add-weight/', views.add_weight, name='add_weight'),
    path('add-measurement/', views.add_measurement, name='add_measurement'),
    path('add-photo/', views.add_photo, name='add_photo'),
    path('delete-weight/<int:pk>/', views.delete_weight, name='delete_weight'),
]
