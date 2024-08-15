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
    drill = models.ForeignKey(
        'Drill',
        on_delete=models.CASCADE,
        related_name='scores'
    )
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


class DrillSet(models.Model):
    """DrillSet object representing a routine of multiple drills"""
    name = models.CharField(max_length=255)
    drills = models.ManyToManyField(Drill, related_name='drill_sets')
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='drill_sets'
    )

    def __str__(self):
        return self.name
    

class DrillSetScore(models.Model):
    """DrillSetScore object representing the scores for a drill set"""
    drill_set = models.ForeignKey(DrillSet, on_delete=models.CASCADE, related_name='set_scores')
    scores = models.ManyToManyField(DrillScore, related_name='drill_set_scores')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='drill_set_scores_created',
        default=888
    )

    def __str__(self):
        return f"Scores for {self.drill_set.name}"
