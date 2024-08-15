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

DRILLSETSCORE_URL = reverse('drillsetScore:drillsetscore-list')

def detail_url(drillSetScoreId):
    """Return drillsetScore detail URL"""
    return reverse('drillsetScore:drillsetscore-detail', args=[drillSetScoreId])

def create_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)

def create_drill(uploadedBy, **params):
    """Create and return a sample drill"""
    defaults = {
        'name': 'Drill 1',
        'maxScore': 10,
        'instructions': 'Test instructions',
        'type': 'standard',
        'skills': ['potting', 'position', 'aim'],
    }
    defaults.update(params)
    return Drill.objects.create(uploadedBy=uploadedBy, **defaults)

def create_drillset(uploadedBy, **params):
    """Create and return a sample drillset"""
    drill1 = create_drill(uploadedBy=uploadedBy)
    drill2 = create_drill(uploadedBy=uploadedBy)
    drill3 = create_drill(uploadedBy=uploadedBy)
    
    drill_set = DrillSet.objects.create(
        name="Example Drill Set",
        user=uploadedBy
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

def create_drillsetscore(**params):
    """Create and return a sample drill set score"""
    user = create_user(
        email='example9@example.com',
        password='password123',
    )
    drill_set = create_drillset(uploadedBy=user)

    scores = []
    for drill in drill_set.drills.all():
        score = create_drillscore(drill=drill, score=5, user=user)
        scores.append(score)

    drillset_score = DrillSetScore.objects.create(
        drill_set=drill_set,
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
            email='example@example.com',
            password='password123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_drillsetScores(self):
        """Test retrieving drillsetScores"""
        create_drillsetscore(drillSet=create_drillset(uploadedBy=self.user), user=self.user)
        create_drillsetscore(drillSet=create_drillset(uploadedBy=self.user), user=self.user)

        res = self.client.get(DRILLSETSCORE_URL)

        drillsetScores = DrillSetScore.objects.all().order_by('id')

        serializer = DrillSetScoreSerializer(drillsetScores, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_drillsetScore_detail(self):
        """Test retrieving a drillsetScore detail"""
        drillsetScore = create_drillsetscore(drillSet=create_drillset(uploadedBy=self.user), user=self.user)

        url = detail_url(drillsetScore.id)
        res = self.client.get(url)

        serializer = DrillSetScoreSerializer(drillsetScore)
        self.assertEqual(res.data, serializer.data)

    def test_create_drillsetScore(self):
        """Test creating a drillsetScore"""
        drillset = create_drillset(uploadedBy=self.user)
        payload = {
            'drillSet': drillset.id,
            'user': self.user.id,
        }
        res = self.client.post(DRILLSETSCORE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        drillsetScore = DrillSetScore.objects.get(id=res.data['id'])
        self.assertEqual(drillsetScore.user, self.user)
        self.assertEqual(drillsetScore.drillSet, drillset)

    def test_create_drillsetScore_with_scores(self):
        """Test creating a drillsetScore with scores"""
        drillset = create_drillset(uploadedBy=self.user)
        drill1 = create_drill(uploadedBy=self.user)
        drill2 = create_drill(uploadedBy=self.user)
        drill3 = create_drill(uploadedBy=self.user)

        score1 = create_drillscore(drill1, 5, user=self.user)
        score2 = create_drillscore(drill2, 7, user=self.user)
        score3 = create_drillscore(drill3, 9, user=self.user)

        payload = {
            'drillSet': drillset.id,
            'user': self.user.id,
            'scores': [score1.id, score2.id, score3.id],
        }
        res = self.client.post(DRILLSETSCORE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        drillsetScore = DrillSetScore.objects.get(id=res.data['id'])
        self.assertEqual(drillsetScore.user, self.user)
        self.assertEqual(drillsetScore.drillSet, drillset)
        self.assertEqual(drillsetScore.scores.count(), 3)

    def test_partial_update_drillsetScore(self):
        """Test updating a drillsetScore with patch"""
        drillsetScore = create_drillsetscore(drillSet=create_drillset(uploadedBy=self.user), user=self.user)
        drill1 = create_drill(uploadedBy=self.user)
        drill2 = create_drill(uploadedBy=self.user)
        drill3 = create_drill(uploadedBy=self.user)

        score1 = create_drillscore(drill1, 5)
        score2 = create_drillscore(drill2, 7)
        score3 = create_drillscore(drill3, 9)

        payload = {
            'scores': [score1.id, score2.id, score3.id],
        }
        url = detail_url(drillsetScore.id)
        self.client.patch(url, payload)

        drillsetScore.refresh_from_db()
        self.assertEqual(drillsetScore.scores.count(), 3)

    def test_full_update_drillsetScore(self):
        """Test updating a drillsetScore with put"""
        drillsetScore = create_drillsetscore(drillSet=create_drillset(uploadedBy=self.user), user=self.user)
        drill1 = create_drill(uploadedBy=self.user)
        drill2 = create_drill(uploadedBy=self.user)
        drill3 = create_drill(uploadedBy=self.user)

        score1 = create_drillscore(drill1, 5)
        score2 = create_drillscore(drill2, 7)
        score3 = create_drillscore(drill3, 9)

        payload = {
            'drillSet': drillsetScore.drillSet.id,
            'user': drillsetScore.user,
            'scores': [score1.id, score2.id, score3.id],
        }
        url = detail_url(drillsetScore.id)
        self.client.put(url, payload)

        drillsetScore.refresh_from_db()
        self.assertEqual(drillsetScore.scores.count(), 3)

    def test_delete_drillsetScore(self):
        """Test deleting a drillsetScore"""
        drillsetScore = create_drillsetscore(drillSet=create_drillset(uploadedBy=self.user))
        url = detail_url(drillsetScore.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DrillSetScore.objects.filter(id=drillsetScore.id).count(), 0)

