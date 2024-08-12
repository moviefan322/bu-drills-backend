"""
Tests for drillScore APIs.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import DrillScore, Drill

from drillScore.serializers import (
    DrillScoreSerializer,
    DrillScoreDetailSerializer,
)

SCORES_URL = reverse('drillScore:drillscore-list')


def detail_url(drillScoreId):
    """Return drillScore detail URL"""
    return reverse('drillScore:drillscore-detail', args=[drillScoreId])


def create_drill_score(user, drill=None, **params):
    """Create and return a sample drillScore"""
    if drill is None:
        drill = Drill.objects.create(
            name='Sample Drill',
            maxScore=10,
            instructions='Sample instructions',
            type='standard'
        )

    defaults = {
        'drill': drill,
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
        create_drill_score(user=self.user)
        create_drill_score(user=self.user)

        res = self.client.get(SCORES_URL)

        drillScores = DrillScore.objects.all().order_by('-id')
        serializer = DrillScoreSerializer(drillScores, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_drillScores_limited_to_user(self):
        """Test that drillScores for the authenticated user are returned"""
        user2 = create_user(email='user2@example.com', password='testpass123')
        create_drill_score(user=user2)
        create_drill_score(user=self.user)

        res = self.client.get(SCORES_URL)

        drills = DrillScore.objects.filter(user=self.user)
        serializer = DrillScoreSerializer(drills, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)

    def test_get_drillScore_detail(self):
        """Test viewing a drillScore detail"""
        drill = create_drill_score(user=self.user)

        url = detail_url(drill.id)
        res = self.client.get(url)

        serializer = DrillScoreDetailSerializer(drill)
        self.assertEqual(res.data, serializer.data)

    def test_create_drill_score(self):
        """Test creating a new drillScore"""
        drill = Drill.objects.create(
            name='Sample Drill',
            maxScore=10,
            instructions='Sample instructions',
            type='standard'
        )

        payload = {
            'drill': drill.id,  # When using API requests, you pass the ID
            'score': 5,
            'maxScore': 10,
        }
        res = self.client.post(SCORES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        drillscore = DrillScore.objects.get(id=res.data['id'])
        # But in your test validation, check the instance
        self.assertEqual(drillscore.drill, drill)
        self.assertEqual(drillscore.score, 5)
        self.assertEqual(drillscore.maxScore, 10)
        self.assertEqual(drillscore.user, self.user)

    def test_partial_update(self):
        """Test updating a drillScore with patch"""
        drill = Drill.objects.create(
            name='Sample Drill',
            maxScore=10,
            instructions='Sample instructions',
            type='standard'
        )
        original_score = 5
        drillscore = create_drill_score(
            user=self.user,
            drill=drill,
            maxScore=10,
            score=original_score
        )

        payload = {
            'maxScore': 15,
        }
        url = detail_url(drillscore.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        drillscore.refresh_from_db()
        self.assertEqual(drillscore.score, 5)
        self.assertEqual(drillscore.maxScore, 15)
        self.assertEqual(drillscore.drill, drill)

    def test_full_update(self):
        """Test full update of drillScore."""
        drill = Drill.objects.create(
            name='Sample Drill',
            maxScore=10,
            instructions='Sample instructions',
            type='standard'
        )
        newdrill = Drill.objects.create(
            name='Sample Drill 2',
            maxScore=10,
            instructions='Sample instructions',
            type='standard'
        )
        drillScore = create_drill_score(
            user=self.user,
            drill=drill,
            score=5,
            maxScore=10,
        )

        # Use newdrill.id instead of passing the whole object
        payload = {
            'drill': newdrill.id,  # Pass the ID of the new drill
            'score': 6,
            'maxScore': 11,
        }

        url = detail_url(drillScore.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        drillScore.refresh_from_db()

        # Check that the drill has been updated to newdrill
        self.assertEqual(drillScore.drill, newdrill)
        self.assertEqual(drillScore.score, payload['score'])
        self.assertEqual(drillScore.maxScore, payload['maxScore'])
        self.assertEqual(drillScore.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the drillScore user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        drillScore = create_drill_score(user=self.user)

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
        drillScore = create_drill_score(user=self.user)

        url = detail_url(drillScore.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DrillScore.objects.filter(id=drillScore.id).exists())

    def test_drillScore_other_users_drillScore_error(self):
        """Test that a user cannot delete another user's drillScore."""
        new_user = create_user(email='user2@example.com', password='pass123')
        drillScore = create_drill_score(user=new_user)

        url = detail_url(drillScore.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(DrillScore.objects.filter(id=drillScore.id).exists())

    def test_retrieve_drillScores_by_drillId(self):
        """Test retrieving drill scores by drillId"""
        drill = Drill.objects.create(
            name='Sample Drill',
            maxScore=10,
            instructions='Sample instructions',
            type='standard'
        )
        drill2 = Drill.objects.create(
            name='Sample Drill 2',
            maxScore=10,
            instructions='Sample instructions',
            type='standard'
        )
        drillscore1 = create_drill_score(user=self.user, drill=drill)
        drillscore2 = create_drill_score(user=self.user, drill=drill)
        user2 = create_user(email='user2@example.com', password='testpass123')
        drillscore3 = create_drill_score(user=user2, drill=drill)
        create_drill_score(user=self.user, drill=drill2)

        # Pass the drill's ID in the reverse function, not the instance itself
        url = reverse(
            'drillScore:drillscore-by_drill',
            kwargs={'drillId': drill.id}  # Use drill.id here
        )
        res = self.client.get(url)

        serializer = DrillScoreSerializer(
            [drillscore1, drillscore2, drillscore3],
            many=True
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_drillScores_by_drillId_with_no_scores(self):
        """Test retrieving drill scores by drillId when there are no scores"""
        drill = Drill.objects.create(
            name='Sample Drill',
            maxScore=10,
            instructions='Sample instructions',
            type='standard'
        )
        url = reverse(
            'drillScore:drillscore-by_drill',
            kwargs={'drillId': drill.id}
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, [])
