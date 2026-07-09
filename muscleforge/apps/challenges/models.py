from django.db import models
from django.conf import settings


class Challenge(models.Model):
    DURATION_CHOICES = [(30, '30 Days'), (60, '60 Days'), (90, '90 Days')]
    DIFFICULTY_CHOICES = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]

    title = models.CharField(max_length=100)
    description = models.TextField()
    duration_days = models.PositiveIntegerField(choices=DURATION_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    xp_reward = models.PositiveIntegerField(default=100)
    badge_image = models.ImageField(upload_to='badges/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class DailyMission(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    xp_reward = models.PositiveIntegerField(default=10)
    mission_type = models.CharField(max_length=30, default='workout')
    target_value = models.FloatField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class UserChallenge(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('completed', 'Completed'), ('failed', 'Failed')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='challenges')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    current_day = models.PositiveIntegerField(default=1)
    progress_percentage = models.FloatField(default=0)

    class Meta:
        unique_together = ['user', 'challenge']

    def __str__(self):
        return f"{self.user.email} - {self.challenge.title}"


class Achievement(models.Model):
    BADGE_CHOICES = [
        ('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    badge_type = models.CharField(max_length=20, choices=BADGE_CHOICES)
    icon = models.CharField(max_length=50, default='🏆')
    xp_reward = models.PositiveIntegerField(default=50)
    requirement_type = models.CharField(max_length=50)
    requirement_value = models.FloatField(default=1)

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'achievement']


class UserXP(models.Model):
    LEVEL_THRESHOLDS = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500, 5500]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='xp')
    total_xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Level {self.level} ({self.total_xp} XP)"

    def add_xp(self, amount):
        self.total_xp += amount
        for i, threshold in enumerate(self.LEVEL_THRESHOLDS):
            if self.total_xp >= threshold:
                self.level = i + 1
        self.save()
