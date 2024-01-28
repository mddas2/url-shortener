from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField( unique=True,
        error_messages={
            'unique': _(
                "A user is already registered with this email address"),
        },
    )
    phone_number = models.CharField(
        max_length=15, null=False, 
        validators=[
            RegexValidator(r'^\d{1,15}$', 'Phone number must be 15 digits Maximum')
        ]
    )
    username = None
    created_date=models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=5,default=1234)
    is_verified = models.BooleanField(default=False)
    ADMIN=1
    USER=2
    ROLE_CHOICES=(
        (USER,'USER'),
        (ADMIN,'ADMIN'),
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, default=2
    )
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['phone_number','first_name','last_name']
    objects =CustomUserManager()
    def __str__(self) -> str:
        return self.email
    
    def role_name(self):
        if self.role==1:
            return 'Admin'
        elif self.role==2:
            return 'User'