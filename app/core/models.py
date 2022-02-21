from typing import Optional

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, \
    BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom User Manager
    """
    def create_user(self, email: str, password: Optional[str], **extra_fields):
        """
        Creates and saves new user
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user models, supports using email instead of username
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'