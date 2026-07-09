from django.db import models
from django.conf import settings


class HabitLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habit_logs')
    date = models.DateField()
    sleep_hours = models.FloatField(null=True, blank=True)
    water_liters = models.FloatField(null=True, blank=True)
    workout_done = models.BooleanField(default=False)
    meditation_minutes = models.PositiveIntegerField(null=True, blank=True)
    walking_steps = models.PositiveIntegerField(null=True, blank=True)
    reading_minutes = models.PositiveIntegerField(null=True, blank=True)
    calories_consumed = models.PositiveIntegerField(null=True, blank=True)
    protein_consumed = models.FloatField(null=True, blank=True)
    mood = models.PositiveIntegerField(null=True, blank=True, help_text='1-10')
    energy_level = models.PositiveIntegerField(null=True, blank=True, help_text='1-10')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.email} - Habits ({self.date})"

    @property
    def completion_score(self):
        fields = [
            self.sleep_hours, self.water_liters, self.workout_done,
            self.meditation_minutes, self.walking_steps, self.calories_consumed,
        ]
        completed = sum(1 for f in fields if f is not None and f is not False)
        return round((completed / len(fields)) * 100)
