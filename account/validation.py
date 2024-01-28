from django.contrib import messages

from .models import CustomUser


def handle_signup_validation(request, email,phone):
    """Validations while creating new users."""
    if CustomUser.objects.filter(email=email).first():
        messages.info(request, f'User with this email: {email} already exists')
        return False
    if CustomUser.objects.filter(phone_number=phone).first():
        messages.info(request, f'User with this username: {phone} already exists')
        return False

    return True