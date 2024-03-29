from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """Manager for our CustomUser Model"""

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email must be entered")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    