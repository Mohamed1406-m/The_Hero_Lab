from django import forms
from .models import WeightLog, BodyMeasurement, ProgressPhoto


class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ['date', 'weight', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Weight (kg)'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class BodyMeasurementForm(forms.ModelForm):
    class Meta:
        model = BodyMeasurement
        fields = ['date', 'chest', 'waist', 'hips', 'arms', 'thighs', 'calves', 'shoulders', 'neck', 'notes']
        widgets = {f: forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
                   for f in ['chest', 'waist', 'hips', 'arms', 'thighs', 'calves', 'shoulders', 'neck']}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        self.fields['notes'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 2})


class ProgressPhotoForm(forms.ModelForm):
    class Meta:
        model = ProgressPhoto
        fields = ['date', 'photo', 'angle', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'angle': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
