from django import forms
from .models import HabitLog


class HabitLogForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = [
            'sleep_hours', 'water_liters', 'workout_done', 'meditation_minutes',
            'walking_steps', 'reading_minutes', 'calories_consumed', 'protein_consumed',
            'mood', 'energy_level', 'notes'
        ]
        widgets = {
            'sleep_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0', 'max': '24'}),
            'water_liters': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'workout_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meditation_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'walking_steps': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'reading_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'calories_consumed': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'protein_consumed': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'mood': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'energy_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
