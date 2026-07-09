from django.db import models
from django.conf import settings


class MuscleGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='muscle_groups/', null=True, blank=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    DIFFICULTY_CHOICES = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]
    CATEGORY_CHOICES = [
        ('strength', 'Strength'), ('cardio', 'Cardio'), ('flexibility', 'Flexibility'),
        ('balance', 'Balance'), ('hiit', 'HIIT'), ('yoga', 'Yoga'),
    ]
    EQUIPMENT_CHOICES = [
        ('none', 'No Equipment'), ('dumbbells', 'Dumbbells'), ('barbell', 'Barbell'),
        ('resistance_bands', 'Resistance Bands'), ('pull_up_bar', 'Pull-up Bar'),
        ('bench', 'Bench'), ('cable_machine', 'Cable Machine'), ('machine', 'Machine'),
        ('kettlebell', 'Kettlebell'), ('bodyweight', 'Bodyweight'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    instructions = models.TextField()
    muscles_worked = models.ManyToManyField(MuscleGroup, related_name='exercises')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    equipment = models.CharField(max_length=30, choices=EQUIPMENT_CHOICES, default='none')
    calories_per_minute = models.FloatField(default=5.0)
    image = models.ImageField(upload_to='exercises/', null=True, blank=True)
    gif = models.FileField(upload_to='exercises/gifs/', null=True, blank=True)
    video_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    PLAN_TYPE_CHOICES = [('home', 'Home Workout'), ('gym', 'Gym Workout'), ('outdoor', 'Outdoor')]
    GOAL_CHOICES = [
        ('muscle_gain', 'Muscle Gain'), ('weight_loss', 'Weight Loss'),
        ('endurance', 'Endurance'), ('strength', 'Strength'), ('flexibility', 'Flexibility'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_plans', null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=Exercise.DIFFICULTY_CHOICES)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    duration_weeks = models.PositiveIntegerField(default=4)
    days_per_week = models.PositiveIntegerField(default=3)
    is_ai_generated = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class WorkoutDay(models.Model):
    DAY_CHOICES = [(i, f'Day {i}') for i in range(1, 8)]

    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='days')
    day_number = models.PositiveIntegerField(choices=DAY_CHOICES)
    name = models.CharField(max_length=100, blank=True)
    focus = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['day_number']
        unique_together = ['plan', 'day_number']

    def __str__(self):
        return f"{self.plan.name} - Day {self.day_number}"


class WorkoutExercise(models.Model):
    workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField(default=3)
    reps = models.CharField(max_length=20, default='10-12')
    rest_seconds = models.PositiveIntegerField(default=60)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class WorkoutSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_sessions')
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.SET_NULL, null=True, blank=True)
    workout_day = models.ForeignKey(WorkoutDay, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    calories_burned = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.date}"


class SessionExercise(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets_completed = models.PositiveIntegerField(default=0)
    reps_completed = models.CharField(max_length=50, blank=True)
    weight_used = models.FloatField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
