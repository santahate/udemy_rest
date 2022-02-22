from typing import Optional

from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, \
    BaseUserManager
from django.db import models
from django.db.models import Model


class UserManager(BaseUserManager):
    """
    Custom User Manager
    """
    def create_user(self, email: str, password: Optional[str], **extra_fields):
        """
        Creates and saves new user
        """
        if not email:
            raise ValueError('User should have email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
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


class Tag(Model):
    """
    Represent user's tag
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
