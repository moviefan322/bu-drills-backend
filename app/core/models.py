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
from django.contrib.auth import get_user_model


def get_default_user():
    """Return the default user with ID 1, create if it doesn't exist."""
    User = get_user_model()
    try:
        return User.objects.get(pk=1)
    except User.DoesNotExist:
        # Create a default user with ID 1 if it doesn't exist
        return User.objects.create(
            pk=1,
            email='admin@admin.com',
            password='admin'
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
    isSet = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)


class Drill(models.Model):
    """Drill object"""

    class DrillType(models.TextChoices):
        PROGRESSIVE = 'progressive', 'Progressive'
        STANDARD = 'standard', 'Standard'
        HIGHSCORE = 'highscore', 'Highscore'
        LAYOUT = 'layout', 'Layout'
        ATTEMPT = 'attempt', 'Attempt'

    name = models.CharField(max_length=255, unique=True)
    maxScore = models.IntegerField()
    instructions = models.TextField()
    image = models.CharField(max_length=255, blank=True, default='')
    type = models.CharField(max_length=255, choices=DrillType.choices)
    skills = models.JSONField(blank=True, null=True)
    attempts = models.IntegerField(blank=True, null=True)
    layouts = models.IntegerField(blank=True, null=True)
    layoutMaxScore = models.IntegerField(blank=True, null=True)
    tableSetup = models.OneToOneField(
        'TableSetup',
        related_name='drill_table_setup',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class TableSetup(models.Model):
    """Table setup configuration for a drill"""

    drill = models.ForeignKey(
        Drill, related_name='table_setups', on_delete=models.CASCADE)
    drillName = models.CharField(max_length=255)
    ballPositionProps = models.JSONField(blank=True, null=True)
    pottingPocketProp = models.JSONField(blank=True, null=True)
    targetSpecs = models.JSONField(blank=True, null=True)
    leaveLineProp = models.JSONField(blank=True, null=True)
    kickShotLineProp = models.JSONField(blank=True, null=True)
    bankShotLineProp = models.JSONField(blank=True, null=True)
    startIndex = models.IntegerField()
    showShotLine = models.BooleanField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically update the drill's tableSetup field
        self.drill.tableSetup = self
        self.drill.save()

    def __str__(self):
        return f"TableSetup for Drill: {self.drill.name}"


class DrillSet(models.Model):
    """DrillSet object representing a routine of multiple drills"""
    name = models.CharField(max_length=255)
    drills = models.ManyToManyField(Drill, related_name='drill_sets')
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='drill_sets',
        default=get_default_user
    )

    def __str__(self):
        return self.name


class DrillSetMembership(models.Model):
    drill = models.ForeignKey(Drill, on_delete=models.CASCADE)
    drill_set = models.ForeignKey(DrillSet, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ['position']


class DrillSetScore(models.Model):
    """DrillSetScore object representing the scores for a drill set"""
    drill_set = models.ForeignKey(
        DrillSet,
        on_delete=models.CASCADE,
        related_name='set_scores'
    )
    scores = models.ManyToManyField(
        DrillScore,
        related_name='drill_set_scores'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='drill_set_scores_created',
        default=get_default_user
    )

    def __str__(self):
        return f"Scores for {self.drill_set.name}"
