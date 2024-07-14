"""
Tests for drillScore APIs.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import DrillScore

from drillScore.serializers import DrillScoreSerializer

SCORES_URL = reverse('drillScore:drillscore-list')

def create_drill(user, **params):
    """Create and return a sample drillScore"""
    defaults = {
        'drillId': 123,
        'score': 5,
        'maxScore': 10,
        'date': 'datestring',
    }
    defaults.update(params)

    drillScore = DrillScore.objects.create(user=user, **defaults)
    return drillScore

class PublicDrillScoreApiTests(TestCase):
    """Test the publicly available drillScore API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving drillScores"""
        res = self.client.get(SCORES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDrillScoreApiTests(TestCase):
    """Test the authorized user drillScore API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_drill(user=self.user)
        create_drill(user=self.user)

        res = self.client.get(SCORES_URL)

        drillScores = DrillScore.objects.all().order_by('-id')
        serializer = DrillScoreSerializer(drillScores, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_drillScores_limited_to_user(self):
        """Test that drillScores for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'user2@example.com',
            'testpass123',
        )
        create_drill(user=user2)
        create_drill(user=self.user)

        res = self.client.get(SCORES_URL)

        drills = DrillScore.objects.filter(user=self.user)
        serializer = DrillScoreSerializer(drills, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)