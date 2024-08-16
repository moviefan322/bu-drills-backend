"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_drill(createdBy, **params):
    """Create and return a sample drill"""
    defaults = {
        'name': 'Sample Drill',
        'maxScore': 10,
        'instructions': 'Test instructions',
        'type': 'standard',
        'skills': ['potting', 'position', 'aim'],
    }
    defaults.update(params)

    return models.Drill.objects.create(createdBy=createdBy, **defaults)


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
        """Test creating a DrillScore is successful"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        drill = models.Drill.objects.create(
            name='Test Drill',
            maxScore=10,
            instructions='Test instructions',
            type='standard',
            skills=['potting', 'position', 'aim'],
            createdBy=user,
        )

        drillScore = models.DrillScore.objects.create(
            user=user,
            drill=drill,  # Use the Drill instance here
            score=5,
            maxScore=10,
        )

        # Assertions
        self.assertEqual(
            drillScore.user,
            user,
            "The user should match the one created"
            )
        self.assertEqual(
            drillScore.drill,
            drill,
            "The drill should match the one created"
            )
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

    def test_create_drill_set(self):
        """Test creating a drill set is successful"""
        user = get_user_model().objects.create_user(
            email='example@example.com',
            password='testpass123',
        )

        drill1 = create_drill(createdBy=user)
        drill2 = create_drill(createdBy=user)

        drill_set = models.DrillSet.objects.create(
            name="Example Drill Set",
            createdBy=user
        )
        drill_set.drills.add(drill1, drill2)

        self.assertEqual(drill_set.name, "Example Drill Set")
        self.assertEqual(drill_set.createdBy, user)
        self.assertEqual(drill_set.drills.count(), 2)
        self.assertIn(drill1, drill_set.drills.all())
        self.assertIn(drill2, drill_set.drills.all())

    def test_create_drill_set_score(self):
        """Test creating a drill set score is successful"""
        user = get_user_model().objects.create_user(
            email='example@example.com',
            password='testpass123',
        )
        drill1 = create_drill(createdBy=user)
        drill2 = create_drill(createdBy=user)

        drill_set = models.DrillSet.objects.create(
            name="Example Drill Set",
            createdBy=user
        )
        drill_set.drills.add(drill1, drill2)

        drill_score1 = models.DrillScore.objects.create(
            user=user,
            drill=drill1,
            score=5,
            maxScore=10,
        )
        drill_score2 = models.DrillScore.objects.create(
            user=user,
            drill=drill2,
            score=8,
            maxScore=10,
        )

        drill_set_score = models.DrillSetScore.objects.create(
            drill_set=drill_set,
        )
        drill_set_score.scores.add(drill_score1, drill_score2)

        # Assertions
        self.assertEqual(drill_set_score.drill_set, drill_set)
        self.assertEqual(drill_set_score.scores.count(), 2)
        self.assertIn(drill_score1, drill_set_score.scores.all())
        self.assertIn(drill_score2, drill_set_score.scores.all())
