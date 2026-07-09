import secrets
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import EmailVerificationToken, PasswordResetToken, UserProfile

User = get_user_model()


def create_user(email, username, password, first_name='', last_name=''):
    user = User.objects.create_user(
        email=email, username=username, password=password,
        first_name=first_name, last_name=last_name
    )
    UserProfile.objects.create(user=user)
    send_verification_email(user)
    return user


def send_verification_email(user):
    token = secrets.token_urlsafe(32)
    EmailVerificationToken.objects.create(user=user, token=token)
    verify_url = f"{settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000'}/accounts/verify-email/{token}/"
    send_mail(
        subject='Verify your MuscleForge AI account',
        message=f'Click to verify: {verify_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )


def verify_email(token):
    try:
        obj = EmailVerificationToken.objects.get(token=token, is_used=False)
        if obj.created_at < timezone.now() - timedelta(hours=24):
            return False, 'Token expired'
        obj.user.is_email_verified = True
        obj.user.save()
        obj.is_used = True
        obj.save()
        return True, 'Email verified'
    except EmailVerificationToken.DoesNotExist:
        return False, 'Invalid token'


def send_password_reset_email(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return False
    token = secrets.token_urlsafe(32)
    PasswordResetToken.objects.create(user=user, token=token)
    reset_url = f"{settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000'}/accounts/reset-password/{token}/"
    send_mail(
        subject='Reset your MuscleForge AI password',
        message=f'Click to reset: {reset_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )
    return True


def reset_password(token, new_password):
    try:
        obj = PasswordResetToken.objects.get(token=token, is_used=False)
        if obj.created_at < timezone.now() - timedelta(hours=1):
            return False, 'Token expired'
        obj.user.set_password(new_password)
        obj.user.save()
        obj.is_used = True
        obj.save()
        return True, 'Password reset'
    except PasswordResetToken.DoesNotExist:
        return False, 'Invalid token'
