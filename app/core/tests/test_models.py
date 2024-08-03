"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_superuser)

    def test_create_drillScore(self):
        """Test creating a drillScore is successful"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        drillScore = models.DrillScore.objects.create(
            user=user,
            drillId=123,
            score=5,
            maxScore=10,
        )

        self.assertEqual(
            drillScore.user,
            user,
            "The user should match the one created"
        )
        self.assertEqual(drillScore.drillId, 123, "The drillId should be 123")
        self.assertEqual(drillScore.score, 5, "The score should be 5")
        self.assertEqual(drillScore.maxScore, 10, "The maxScore should be 10")

    def test_create_drill(self):
        """Test creating a drill is successful"""
        drill = models.Drill.objects.create(
            name="Example Drill",
            maxScore=100,
            instructions="Do this drill carefully.",
            type="standard",
            skills=["running", "jumping"],
            layoutMaxScore=20,
        )

        self.assertEqual(drill.name, "Example Drill")
        self.assertEqual(drill.maxScore, 100)
        self.assertEqual(drill.instructions, "Do this drill carefully.")
        self.assertEqual(drill.type, "standard")
        self.assertEqual(drill.skills, ["running", "jumping"])
        self.assertIsNone(drill.attempts)
        self.assertIsNone(drill.layouts)
        self.assertEqual(drill.layoutMaxScore, 20)

    def test_create_drill_with_optional_fields(self):
        """Test creating a drill with optional fields"""
        drill = models.Drill.objects.create(
            name="Example Drill",
            maxScore=100,
            instructions="Do this drill carefully.",
            type="layout",
            skills=["coordination", "endurance"],
            attempts=3,
            layouts=2,
            layoutMaxScore=50,
        )

        self.assertEqual(drill.name, "Example Drill")
        self.assertEqual(drill.maxScore, 100)
        self.assertEqual(drill.instructions, "Do this drill carefully.")
        self.assertEqual(drill.type, "layout")
        self.assertEqual(drill.skills, ["coordination", "endurance"])
        self.assertEqual(drill.attempts, 3)
        self.assertEqual(drill.layouts, 2)
        self.assertEqual(drill.layoutMaxScore, 50)