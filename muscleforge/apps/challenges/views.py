from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from django.contrib import messages
from .models import Challenge, UserChallenge, Achievement, UserAchievement, UserXP, DailyMission


@method_decorator(login_required, name='dispatch')
class ChallengeListView(View):
    template_name = 'challenges/list.html'

    def get(self, request):
        challenges = Challenge.objects.filter(is_active=True)
        user_challenges = UserChallenge.objects.filter(user=request.user).select_related('challenge')
        joined_ids = list(user_challenges.values_list('challenge_id', flat=True))
        xp, _ = UserXP.objects.get_or_create(user=request.user)
        user_achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement')
        achievements = Achievement.objects.all()
        earned = list(user_achievements.values_list('achievement_id', flat=True))
        return render(request, self.template_name, {
            'challenges': challenges,
            'user_challenges': user_challenges,
            'joined_ids': joined_ids,
            'xp': xp,
            'achievements': achievements,
            'earned': earned,
        })


@login_required
def join_challenge(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk, is_active=True)
    uc, created = UserChallenge.objects.get_or_create(user=request.user, challenge=challenge)
    if created:
        messages.success(request, f'Joined "{challenge.title}"! Good luck! 💪')
    else:
        messages.info(request, 'You already joined this challenge.')
    return redirect('challenges:list')


@method_decorator(login_required, name='dispatch')
class MyChallengesView(View):
    template_name = 'challenges/my_challenges.html'

    def get(self, request):
        user_challenges = UserChallenge.objects.filter(
            user=request.user
        ).select_related('challenge').order_by('-started_at')
        xp, _ = UserXP.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {'user_challenges': user_challenges, 'xp': xp})


@method_decorator(login_required, name='dispatch')
class AchievementsView(View):
    template_name = 'challenges/achievements.html'

    def get(self, request):
        all_achievements = Achievement.objects.all()
        earned = list(
            UserAchievement.objects.filter(user=request.user).values_list('achievement_id', flat=True)
        )
        xp, _ = UserXP.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {
            'achievements': all_achievements,
            'earned': earned,
            'xp': xp,
        })