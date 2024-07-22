"""
Tests for drillScore APIs.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import DrillScore

from drillScore.serializers import (
    DrillScoreSerializer,
    DrillScoreDetailSerializer,
)

SCORES_URL = reverse('drillScore:drillscore-list')

def detail_url(drillScoreId):
    """Return drillScore detail URL"""
    return reverse('drillScore:drillscore-detail', args=[drillScoreId])


def create_drill(user, **params):
    """Create and return a sample drillScore"""
    defaults = {
        'drillId': 123,
        'score': 5,
        'maxScore': 10,
    }
    defaults.update(params)

    drillScore = DrillScore.objects.create(user=user, **defaults)
    return drillScore


def create_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_drillScores(self):
        """Test retrieving a list of drillScores."""
        create_drill(user=self.user)
        create_drill(user=self.user)

        res = self.client.get(SCORES_URL)

        drillScores = DrillScore.objects.all().order_by('-id')
        serializer = DrillScoreSerializer(drillScores, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_drillScores_limited_to_user(self):
        """Test that drillScores for the authenticated user are returned"""
        user2 = create_user(email='user2@example.com', password='testpass123')
        create_drill(user=user2)
        create_drill(user=self.user)

        res = self.client.get(SCORES_URL)

        drills = DrillScore.objects.filter(user=self.user)
        serializer = DrillScoreSerializer(drills, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)

    def test_get_drillScore_detail(self):
        """Test viewing a drillScore detail"""
        drill = create_drill(user=self.user)

        url = detail_url(drill.id)
        res = self.client.get(url)

        serializer = DrillScoreDetailSerializer(drill)
        self.assertEqual(res.data, serializer.data)

    def test_create_drillScore(self):
        """Test creating a new drillScore"""
        payload = {
            'drillId': 123,
            'score': 5,
            'maxScore': 10,
        }
        res = self.client.post(SCORES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        drill = DrillScore.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(v, getattr(drill, k))
        self.assertEqual(drill.user, self.user)

    def test_partial_update(self):
        """Test updating a drillScore with patch"""
        original_score = 5
        drill = create_drill(
            user=self.user,
            drillId=123,
            maxScore=10,
            score=original_score
        )

        payload = {
            'maxScore': 15,
        }
        url = detail_url(drill.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        drill.refresh_from_db()
        self.assertEqual(drill.score, 5)
        self.assertEqual(drill.maxScore, 15)
        self.assertEqual(drill.drillId, 123)

    def test_full_update(self):
        """Test full update of drillScore."""
        drillScore = create_drill(
            user=self.user,
            drillId=123,
            score=5,
            maxScore=10,
        )

        payload = {
            'drillId': 124,
            'score': 6,
            'maxScore': 11,
        }

        url = detail_url(drillScore.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        drillScore.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(v, getattr(drillScore, k))
        self.assertEqual(drillScore.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the drillScore user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        drillScore = create_drill(user=self.user)

        payload = {
            'user': new_user.id,
        }
        url = detail_url(drillScore.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        drillScore.refresh_from_db()
        self.assertEqual(drillScore.user, self.user)

    def test_delete_drillScore(self):
        """Test deleting a drillScore."""
        drillScore = create_drill(user=self.user)

        url = detail_url(drillScore.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DrillScore.objects.filter(id=drillScore.id).exists())

    def test_drillScore_other_users_drillScore_error(self):
        """Test that a user cannot delete another user's drillScore."""
        new_user = create_user(email='user2@example.com', password='pass123')
        drillScore = create_drill(user=new_user)

        url = detail_url(drillScore.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(DrillScore.objects.filter(id=drillScore.id).exists())

    def test_retrieve_drillScores_by_drillId(self):
        """Test retrieving drill scores by drillId"""
        drillId = 123
        drill1 = create_drill(user=self.user, drillId=drillId)
        drill2 = create_drill(user=self.user, drillId=drillId)
        create_drill(user=self.user, drillId=456)  # Different drillId

        url = reverse('drillScore:drillscores-by-drill', args=[drillId])
        res = self.client.get(url)

        serializer = DrillScoreSerializer([drill1, drill2], many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_drillScores_by_drillId_limited_to_user(self):
        """Test that only drill scores for the authenticated user are returned"""
        drillId = 123
        user2 = create_user(email='user2@example.com', password='testpass123')
        create_drill(user=user2, drillId=drillId)
        drill = create_drill(user=self.user, drillId=drillId)

        url = reverse('drillScore:drillscores-by-drill', args=[drillId])
        res = self.client.get(url)

        serializer = DrillScoreSerializer([drill], many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)