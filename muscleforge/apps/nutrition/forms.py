from django import forms
from .models import MealLog, WaterLog


class MealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = ['date', 'meal_type', 'food', 'quantity']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'food': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }


class WaterLogForm(forms.ModelForm):
    class Meta:
        model = WaterLog
        fields = ['date', 'amount_ml']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount_ml': forms.NumberInput(attrs={'class': 'form-control'}),
        }
