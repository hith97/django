from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random
import string

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'Super Admin'
        ORG_ADMIN = 'ORG_ADMIN', 'Organization Admin'
        REVIEWER = 'REVIEWER', 'Reviewer'
        USER = 'USER', 'User'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text='Phone number of the user'
    )

    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def is_superadmin(self):
        return self.role == self.Role.SUPERADMIN

    def is_org_admin(self):
        return self.role == self.Role.ORG_ADMIN

    def is_reviewer(self):
        return self.role == self.Role.REVIEWER

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=6))

    def is_valid(self):
        # OTP valid for 10 minutes
        return (not self.is_used and 
                timezone.now() <= self.created_at + timezone.timedelta(minutes=10))
