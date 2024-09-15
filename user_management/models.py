import django.utils.timezone
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        user = self.model(email=email, is_active=True, **kwargs)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        return self._create_user(email, password, **kwargs)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=255)
    created_date = models.DateTimeField(default=django.utils.timezone.now)  # Fix here
    last_login = models.DateTimeField(null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Avoid conflict with default User model
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Avoid conflict with default User model
        blank=True,
        help_text='Specific permissions for this user.'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'  # Add this line

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Add self.password here
