import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import StreamingHttpResponse, JsonResponse
from django.contrib import messages
from .models import ChatSession, ChatMessage, AIReport
from .services import stream_chat_with_ai, chat_with_ai, generate_diet_plan, generate_ai_report


@method_decorator(login_required, name='dispatch')
class AIChatView(View):
    template_name = 'ai_coach/chat.html'
    suggested_prompts = [
        "What should I eat right now to hit my calorie goal?",
        "Did I do enough today? What's missing?",
        "Give me a quick high-calorie Indian meal idea",
        "Should I workout today or rest?",
    ]

    def get(self, request):
        # Only show sessions that have at least one message
        sessions = ChatSession.objects.filter(user=request.user, messages__isnull=False).distinct()[:10]
        session_id = request.GET.get('session')
        current_session = None
        chat_messages = []

        if session_id:
            current_session = get_object_or_404(ChatSession, id=session_id, user=request.user)
            chat_messages = current_session.messages.all()

        return render(request, self.template_name, {
            'sessions': sessions,
            'current_session': current_session,
            'chat_messages': chat_messages,
            'suggested_prompts': self.suggested_prompts,
        })


@login_required
def stream_chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        session_id = data.get('session_id')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not message:
        return JsonResponse({'error': 'Message required'}, status=400)

    if not hasattr(request, '_dont_enforce_csrf_checks'):
        pass  # CSRF handled by Django middleware

    response = StreamingHttpResponse(
        stream_chat_with_ai(request.user, message, session_id),
        content_type='text/event-stream'
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


@login_required
def new_session(request):
    session = ChatSession.objects.create(user=request.user, title='New Chat')
    return JsonResponse({'session_id': session.id})


@login_required
def delete_session(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    session.delete()
    return redirect('ai_coach:chat')


@method_decorator(login_required, name='dispatch')
class DietPlanView(View):
    template_name = 'ai_coach/diet_plan.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        plan = generate_diet_plan(request.user)
        return render(request, self.template_name, {'plan': plan})


@method_decorator(login_required, name='dispatch')
class AIReportView(View):
    template_name = 'ai_coach/report.html'

    def get(self, request):
        reports = AIReport.objects.filter(user=request.user)[:5]
        return render(request, self.template_name, {'reports': reports})

    def post(self, request):
        report_type = request.POST.get('report_type', 'weekly')
        content = generate_ai_report(request.user, report_type)
        from django.utils import timezone
        from datetime import timedelta
        end = timezone.now().date()
        start = end - timedelta(days=7 if report_type == 'weekly' else 30)
        report = AIReport.objects.create(
            user=request.user, report_type=report_type,
            content=content, period_start=start, period_end=end
        )
        messages.success(request, 'AI Report generated!')
        return render(request, self.template_name, {
            'reports': AIReport.objects.filter(user=request.user)[:5],
            'latest_report': report,
        })


@login_required
def delete_report(request, report_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    report = get_object_or_404(AIReport, id=report_id, user=request.user)
    report.delete()
    return JsonResponse({'status': 'ok'})