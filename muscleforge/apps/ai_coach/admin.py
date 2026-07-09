from django.contrib import admin
from .models import ChatSession, ChatMessage, AIReport


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'title']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'created_at']
    list_filter = ['role']


@admin.register(AIReport)
class AIReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'report_type', 'period_start', 'period_end', 'created_at']
    list_filter = ['report_type']
