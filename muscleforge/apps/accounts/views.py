from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, ForgotPasswordForm, ResetPasswordForm, ChangePasswordForm
from .services import create_user, verify_email, send_password_reset_email, reset_password
from .models import UserProfile


class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return render(request, self.template_name, {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            login(request, user)
            messages.success(request, 'Account created! Please verify your email.')
            return redirect('dashboard:home')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'dashboard:home')
            return redirect(next_url)
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('accounts:login')


class VerifyEmailView(View):
    def get(self, request, token):
        success, msg = verify_email(token)
        if success:
            messages.success(request, msg)
        else:
            messages.error(request, msg)
        return redirect('accounts:login')


class ForgotPasswordView(View):
    template_name = 'accounts/forgot_password.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ForgotPasswordForm()})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            send_password_reset_email(form.cleaned_data['email'])
            messages.success(request, 'If that email exists, a reset link has been sent.')
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})


class ResetPasswordView(View):
    template_name = 'accounts/reset_password.html'

    def get(self, request, token):
        return render(request, self.template_name, {'form': ResetPasswordForm(), 'token': token})

    def post(self, request, token):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            success, msg = reset_password(token, form.cleaned_data['password1'])
            if success:
                messages.success(request, 'Password reset! Please login.')
                return redirect('accounts:login')
            messages.error(request, msg)
        return render(request, self.template_name, {'form': form, 'token': token})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = ProfileUpdateForm(instance=profile, user=request.user)
        return render(request, self.template_name, {'form': form, 'profile': profile})

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        action = request.POST.get('form_action')
        if action == 'personal':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            if first_name:
                request.user.first_name = first_name
            if last_name:
                request.user.last_name = last_name
            request.user.save()
            if 'avatar' in request.FILES:
                request.user.avatar = request.FILES['avatar']
                request.user.save(update_fields=['avatar'])
            messages.success(request, 'Personal info updated!')
            return redirect('accounts:profile')
        else:
            form = ProfileUpdateForm(request.POST, request.FILES, instance=profile, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Goals & settings saved!')
                return redirect('accounts:profile')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return render(request, self.template_name, {'form': form, 'profile': profile})


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    template_name = 'accounts/change_password.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ChangePasswordForm()})

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if not request.user.check_password(form.cleaned_data['old_password']):
                messages.error(request, 'Current password is incorrect.')
            else:
                request.user.set_password(form.cleaned_data['new_password1'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully!')
                return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})
