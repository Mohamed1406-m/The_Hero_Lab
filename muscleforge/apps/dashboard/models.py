from django.db import models


class DashboardWidget(models.Model):
    """Placeholder model for dashboard app"""
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'dashboard'
