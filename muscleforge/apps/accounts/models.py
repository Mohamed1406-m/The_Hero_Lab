from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/default-avatar.png'


class UserProfile(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('weight_gain', 'Weight Gain'),
        ('maintenance', 'Maintenance'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility'),
    ]
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('lightly_active', 'Lightly Active'),
        ('moderately_active', 'Moderately Active'),
        ('very_active', 'Very Active'),
        ('extra_active', 'Extra Active'),
    ]
    DIET_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('non_vegetarian', 'Non-Vegetarian'),
        ('eggetarian', 'Eggetarian'),
        ('keto', 'Keto'),
        ('paleo', 'Paleo'),
    ]
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    height = models.FloatField(null=True, blank=True, help_text='Height in cm')
    weight = models.FloatField(null=True, blank=True, help_text='Weight in kg')
    goal_weight = models.FloatField(null=True, blank=True, help_text='Goal weight in kg')
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='maintenance')
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='moderately_active')
    diet_type = models.CharField(max_length=20, choices=DIET_CHOICES, default='non_vegetarian')
    workout_experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='beginner')
    budget = models.PositiveIntegerField(null=True, blank=True, help_text='Monthly budget in INR')
    medical_conditions = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    daily_calorie_goal = models.PositiveIntegerField(default=2000)
    daily_protein_goal = models.PositiveIntegerField(default=150)
    daily_water_goal = models.FloatField(default=3.0, help_text='Liters')
    daily_steps_goal = models.PositiveIntegerField(default=10000)
    theme = models.CharField(max_length=10, default='dark', choices=[('dark', 'Dark'), ('light', 'Light')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.user.email} Profile"

    @property
    def bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 1)
        return None

    @property
    def bmi_category(self):
        bmi = self.bmi
        if not bmi:
            return 'Unknown'
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal'
        elif bmi < 30:
            return 'Overweight'
        return 'Obese'

    @property
    def tdee(self):
        """Total Daily Energy Expenditure"""
        if not all([self.weight, self.height, self.age, self.gender]):
            return self.daily_calorie_goal
        if self.gender == 'M':
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        multipliers = {
            'sedentary': 1.2, 'lightly_active': 1.375,
            'moderately_active': 1.55, 'very_active': 1.725, 'extra_active': 1.9
        }
        return round(bmr * multipliers.get(self.activity_level, 1.55))


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'email_verification_tokens'


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'password_reset_tokens'
