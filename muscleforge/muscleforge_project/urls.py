from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="MuscleForge AI API",
        default_version='v1',
        description="AI-Powered Fitness Application API",
        contact=openapi.Contact(email="api@muscleforge.ai"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('workout/', include('apps.workout.urls')),
    path('nutrition/', include('apps.nutrition.urls')),
    path('ai-coach/', include('apps.ai_coach.urls')),
    path('progress/', include('apps.progress.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('challenges/', include('apps.challenges.urls')),
    path('blog/', include('apps.blog.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('api/v1/', include('apps.api.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('apps.dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "MuscleForge AI Admin"
admin.site.site_title = "MuscleForge AI"
admin.site.index_title = "Administration"
