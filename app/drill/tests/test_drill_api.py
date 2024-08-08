"""
Tests for drill APIs.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Drill

from drill.serializers import DrillSerializer


DRILLS_URL = reverse('drill:drill-list')


def create_drill(**params):
    """Create and return a sample drill"""
    defaults = {
        'name': 'Drill 1',
        'maxScore': 10,
        'instructions': 'Suck me off',
        'type': 'standard',
        'skills': ['potting', 'position', 'aim'],
    }
    defaults.update(params)

    drill = Drill.objects.create(**defaults)
    return drill


def create_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)


class PublicDrillScoreApiTests(TestCase):
    """Test the drill API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_drills(self):
        """Test retrieving a list of drillScores."""
        create_drill()
        create_drill()

        res = self.client.get(DRILLS_URL)

        drillScores = Drill.objects.all().order_by('-id')
        serializer = DrillSerializer(drillScores, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
