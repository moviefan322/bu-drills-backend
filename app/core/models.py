"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save, and return a new user."""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class DrillScore(models.Model):
    """DrillScore object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    drillId = models.IntegerField()
    score = models.IntegerField()
    maxScore = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)


class Drill(models.Model):
    """Drill object"""

    class DrillType(models.TextChoices):
        PROGRESSIVE = 'progressive', 'Progressive'
        STANDARD = 'standard', 'Standard'
        HIGHSCORE = 'highscore', 'Highscore'
        LAYOUT = 'layout', 'Layout'
        ATTEMPT = 'attempt', 'Attempt'

    name = models.CharField(max_length=255)
    maxScore = models.IntegerField()
    instructions = models.TextField()
    image = models.CharField(max_length=255, blank=True, default='')
    type = models.CharField(max_length=255, choices=DrillType.choices)
    skills = models.JSONField(blank=True, null=True)
    attempts = models.IntegerField(blank=True, null=True)
    layouts = models.IntegerField(blank=True, null=True)
    layoutMaxScore = models.IntegerField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    uploadedBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
