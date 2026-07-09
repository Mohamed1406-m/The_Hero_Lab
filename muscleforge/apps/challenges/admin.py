from django.contrib import admin
from .models import Challenge, DailyMission, UserChallenge, Achievement, UserAchievement, UserXP


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration_days', 'difficulty', 'xp_reward', 'is_active']
    list_filter = ['duration_days', 'difficulty', 'is_active']
    search_fields = ['title']


@admin.register(DailyMission)
class DailyMissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'mission_type', 'xp_reward', 'is_active']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'badge_type', 'xp_reward', 'requirement_type', 'requirement_value']


@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'status', 'current_day', 'progress_percentage']
    list_filter = ['status']


@admin.register(UserXP)
class UserXPAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_xp', 'level']
    search_fields = ['user__email']
