"""
Tests for drillsetScore APIs.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import DrillSet, Drill, DrillSetScore, DrillScore

from drillsetScore.serializers import DrillSetScoreSerializer

import random
import string


DRILLSETSCORE_URL = reverse('drillsetScore:drillsetscore-list')


def detail_url(drillSetScoreId):
    """Return drillsetScore detail URL"""
    return reverse(
        'drillsetScore:drillsetscore-detail',
        args=[drillSetScoreId]
    )


def create_user(**params):
    """Create and return a sample user with a unique email"""
    unique_email = f"user{random.randint(1, 10000)}@example.com"
    return get_user_model().objects.create_user(email=unique_email, **params)


def random_string(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def create_drill(createdBy, **params):
    """Create and return a sample drill"""
    defaults = {
        'name': random_string(),
        'maxScore': 10,
        'instructions': 'Test instructions',
        'type': 'standard',
        'skills': ['potting', 'position', 'aim'],
    }
    defaults.update(params)
    return Drill.objects.create(createdBy=createdBy, **defaults)


def create_drillset(createdBy, **params):
    """Create and return a sample drillset"""
    drill1 = create_drill(createdBy=createdBy)
    drill2 = create_drill(createdBy=createdBy)
    drill3 = create_drill(createdBy=createdBy)

    drill_set = DrillSet.objects.create(
        name="Example Drill Set",
        createdBy=createdBy
    )
    drill_set.drills.add(drill1, drill2, drill3)

    return drill_set  # Return the created drill set


def create_drillscore(drill, score, user, **params):
    """Create and return a sample drill score"""
    defaults = {
        'score': score,
        'maxScore': drill.maxScore,
        'user': user,
    }
    defaults.update(params)
    return DrillScore.objects.create(drill=drill, **defaults)


def create_drillsetscore(user, **params):
    """Create and return a sample drill set score"""
    drill_set = create_drillset(createdBy=user)

    scores = []
    for drill in drill_set.drills.all():
        score = create_drillscore(drill=drill, score=5, user=user)
        scores.append(score)

    drillset_score = DrillSetScore.objects.create(
        drill_set=drill_set,
        user=user,
        **params
    )
    drillset_score.scores.set(scores)

    return drillset_score


class PublicDrillSetScoreApiTests(TestCase):
    """Test the publicly available drillsetScore API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving drillsetScores"""
        res = self.client.get(DRILLSETSCORE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDrillSetScoreApiTests(TestCase):
    """Test the authorized user drillsetScore API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            password='password123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_drillsetScores(self):
        """Test retrieving drillsetScores"""
        create_drillsetscore(user=self.user)
        create_drillsetscore(user=self.user)

        res = self.client.get(DRILLSETSCORE_URL)

        drillsetScores = DrillSetScore.objects.filter(
            user=self.user
        ).order_by('-id')
        serializer = DrillSetScoreSerializer(drillsetScores, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_drillsetScore_detail(self):
        """Test retrieving a drillsetScore detail"""
        drillsetScore = create_drillsetscore(user=self.user)

        url = detail_url(drillsetScore.id)
        res = self.client.get(url)

        serializer = DrillSetScoreSerializer(drillsetScore)
        self.assertEqual(res.data, serializer.data)

    def test_create_drillsetScore_with_scores(self):
        """Test creating a drillsetScore with scores"""
        drillset = create_drillset(createdBy=self.user)

        drill1 = create_drill(createdBy=self.user)
        drill2 = create_drill(createdBy=self.user)
        drill3 = create_drill(createdBy=self.user)

        score1 = {
            "drill": drill1.id,
            "score": 5,
            "maxScore": drill1.maxScore,
        }
        score2 =  {
            "drill": drill2.id,
            "score": 6,
            "maxScore": drill2.maxScore,
        }
        score3 = {
            "drill": drill3.id,
            "score": 7,
            "maxScore": drill3.maxScore,
        }

        cumulative_score = score1['score'] + score2['score'] + score3['score']
        cumulative_max_score = score1['maxScore'] + score2['maxScore'] + score3['maxScore']

        payload = {
            'drill_set': drillset.id,
            'scores': [score1, score2, score3],
        }
        res = self.client.post(DRILLSETSCORE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        drillsetScore = DrillSetScore.objects.get(id=res.data['id'])
        self.assertEqual(drillsetScore.user, self.user)
        self.assertEqual(drillsetScore.drill_set, drillset)
        self.assertEqual(drillsetScore.scores.count(), 3)
        self.assertEqual(drillsetScore.total_score, cumulative_score)
        self.assertEqual(drillsetScore.total_max_score, cumulative_max_score)

    def test_partial_update_drillsetScore(self):
        """Test updating a drillsetScore with patch"""
        drillsetScore = create_drillsetscore(user=self.user)
        drill1 = create_drill(createdBy=self.user)
        drill2 = create_drill(createdBy=self.user)
        drill3 = create_drill(createdBy=self.user)

        # Ensure to pass the user when creating drill scores
        score1 = {
            "drill": drill1.id,
            "score": 5,
            "maxScore": drill1.maxScore,
            }
        score2 =  {
            "drill": drill2.id,
            "score": 6,
            "maxScore": drill1.maxScore,
            }
        score3 = {
            "drill": drill3.id,
            "score": 7,
            "maxScore": drill1.maxScore,
            }

        payload = {
            'scores': [score1, score2, score3],
        }

        url = detail_url(drillsetScore.id)
        self.client.patch(url, payload)

        drillsetScore.refresh_from_db()
        self.assertEqual(drillsetScore.scores.count(), 3)

    def test_full_update_drillsetScore(self):
        """Test updating a drillsetScore with put"""
        drillsetScore = create_drillsetscore(user=self.user)
        drill1 = create_drill(createdBy=self.user)
        drill2 = create_drill(createdBy=self.user)
        drill3 = create_drill(createdBy=self.user)

        score1 = {
            "drill": drill1.id,
            "score": 5,
            "maxScore": drill1.maxScore,
            }
        score2 =  {
            "drill": drill2.id,
            "score": 6,
            "maxScore": drill1.maxScore,
            }
        score3 = {
            "drill": drill3.id,
            "score": 7,
            "maxScore": drill1.maxScore,
            }

        payload = {
            'drill_set': drillsetScore.drill_set.id,
            'user': drillsetScore.user,
            'scores': [score1, score2, score3],
        }

        url = detail_url(drillsetScore.id)
        self.client.put(url, payload)

        drillsetScore.refresh_from_db()
        self.assertEqual(drillsetScore.scores.count(), 3)

    def test_delete_drillsetScore(self):
        """Test deleting a drillsetScore"""
        drillsetScore = create_drillsetscore(user=self.user)
        url = detail_url(drillsetScore.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DrillSetScore.objects.filter(
            id=drillsetScore.id
        ).count(), 0)
