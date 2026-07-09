from django import forms
from .models import WorkoutSession, WorkoutPlan


class WorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ['name', 'date', 'duration_minutes', 'calories_burned', 'notes', 'workout_plan']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'workout_plan': forms.Select(attrs={'class': 'form-select'}),
        }


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['name', 'description', 'plan_type', 'difficulty', 'goal', 'duration_weeks', 'days_per_week']
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'}) for f in ['name', 'duration_weeks', 'days_per_week']}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['plan_type', 'difficulty', 'goal']:
            self.fields[field].widget.attrs['class'] = 'form-select'
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
