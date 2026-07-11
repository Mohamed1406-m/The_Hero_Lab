from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = [
            'age', 'gender', 'height', 'weight', 'goal_weight', 'goal',
            'activity_level', 'diet_type', 'workout_experience', 'budget',
            'medical_conditions', 'bio', 'city', 'daily_calorie_goal',
            'daily_protein_goal', 'daily_water_goal', 'daily_steps_goal', 'theme'
        ]
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'}) for f in ['age', 'height', 'weight', 'goal_weight', 'budget', 'city']}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
        select_fields = ['gender', 'goal', 'activity_level', 'diet_type', 'workout_experience', 'theme']
        for field in select_fields:
            self.fields[field].widget.attrs['class'] = 'form-select'
        textarea_fields = ['medical_conditions', 'bio']
        for field in textarea_fields:
            self.fields[field].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        number_fields = ['daily_calorie_goal', 'daily_protein_goal', 'daily_water_goal', 'daily_steps_goal']
        for field in number_fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError("Passwords don't match.")
        return cleaned_data


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password1') != cleaned_data.get('new_password2'):
            raise forms.ValidationError("New passwords don't match.")
        return cleaned_data
