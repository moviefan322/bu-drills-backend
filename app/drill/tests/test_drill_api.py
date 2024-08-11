"""
Tests for drill APIs.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Drill, Skill

import json

from drill.serializers import DrillSerializer, DrillDetailSerializer


DRILLS_URL = reverse('drill:drill-list')


def detail_url(drillId):
    """Return drill detail URL"""
    return reverse('drill:drill-detail', args=[drillId])


def create_drill(uploadedBy, **params):
    """Create and return a sample drill"""
    skill_names = ['potting', 'position', 'aim']
    
    skill_names = params.pop('skills', skill_names)

    skills = [Skill.objects.get_or_create(name=name)[0] for name in skill_names]

    # Remaining params for the Drill model creation
    defaults = {
        'name': 'Drill 1',
        'maxScore': 10,
        'instructions': 'Default instructions',
        'type': 'standard',
    }
    defaults.update(params)

    drill = Drill.objects.create(uploadedBy=uploadedBy, **defaults)
    
    drill.skills.set(skills)
    
    return drill

def prepare_drill_payload(skill_names=None, **kwargs):
    """
    Prepare the drill payload with skill IDs.
    :param skill_names: A list of skill names. Defaults to ['potting', 'position', 'aim'].
    :param kwargs: Additional fields to include in the payload.
    :return: A payload dictionary ready for use in API requests.
    """
    if skill_names is None:
        skill_names = ['potting', 'position', 'aim']

    skills = [Skill.objects.get_or_create(name=name)[0] for name in skill_names]

    payload = {
        'name': 'Drill 1',
        'maxScore': 10,
        'instructions': 'Test instructions',
        'type': 'standard',
        'skills': [skill.id for skill in skills],  # Use skill IDs
    }
    payload.update(kwargs)
    return payload


def create_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)


class PublicDrillScoreApiTests(TestCase):
    """Test the drill API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required for creating a drill"""
        payload = prepare_drill_payload()

        # Make an unauthenticated POST request
        client = APIClient()
        res = client.post(DRILLS_URL, payload)

        # Assert that the response status code is 401 Unauthorized
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_retrieve_drills(self):
        """Test retrieving a list of drillScores."""
        create_drill(uploadedBy=create_user(email='example@example.com'))
        create_drill(uploadedBy=create_user(email='example2@example.com'))

        res = self.client.get(DRILLS_URL)

        drillScores = Drill.objects.all().order_by('-id')
        serializer = DrillSerializer(drillScores, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_drill_detail(self):
        """Test viewing a drill detail"""
        drill = create_drill(uploadedBy=create_user(
            email='example@example.com'
            ))

        url = detail_url(drill.id)
        res = self.client.get(url)

        serializer = DrillDetailSerializer(drill)
        self.assertEqual(res.data, serializer.data)


class PrivateDrillApiTests(TestCase):
    """Test the authorized user drill API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    from rest_framework import status

    def test_create_drill_authenticated(self):
        """Test creating a drill with authentication"""
        payload = prepare_drill_payload()

        # Make an authenticated POST request
        res = self.client.post(DRILLS_URL, payload)

        # Assert that the drill was created successfully
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Fetch the created drill from the database
        drill = Drill.objects.get(id=res.data['id'])

        # Assert that the drill attributes match the payload
        self.assertEqual(drill.name, payload['name'])
        self.assertEqual(drill.maxScore, payload['maxScore'])
        self.assertEqual(drill.instructions, payload['instructions'])
        self.assertEqual(drill.type, payload['type'])
        self.assertEqual(list(drill.skills.all()), skills)  # Ensure skills are correctly associated

    def test_create_drill(self):
        """Test creating a new drill"""
        # Create some skill objects in the database
        payload = prepare_drill_payload()

        # Make an authenticated POST request to create the drill
        res = self.client.post(DRILLS_URL, payload)

        # Assert that the drill was created successfully
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Fetch the created drill from the database
        drill = Drill.objects.get(id=res.data['id'])

        # Assert that the drill attributes match the payload
        for k, v in payload.items():
            if k == 'skills':
                # Check that the associated skills match the payload skills
                self.assertEqual(list(drill.skills.values_list('id', flat=True)), v)
            else:
                self.assertEqual(v, getattr(drill, k))

        # Assert that the uploadedBy field is correctly set to the authenticated user
        self.assertEqual(drill.uploadedBy, self.user)


    def test_update_drill_not_owned(self):
        """Test that trying to update a drill not owned by the user fails"""
        other_user = create_user(
            email='other@example.com',
            password='password123',
        )
        drill = create_drill(uploadedBy=other_user)

        payload = {'name': 'Updated Drill Name'}
        url = detail_url(drill.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        drill.refresh_from_db()
        self.assertNotEqual(drill.name, payload['name'])

    def test_delete_drill_not_owned(self):
        """Test that trying to delete a drill not owned by the user fails"""
        other_user = create_user(
            email='other@example.com',
            password='password123',
        )
        drill = create_drill(uploadedBy=other_user)

        url = detail_url(drill.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Drill.objects.filter(id=drill.id).exists())

    def test_uploadedBy_is_set_automatically(self):
        """
        Test that uploadedBy is automatically set to the authenticated user
        """
        payload = prepare_drill_payload()

        # Make an authenticated POST request to create the drill
        res = self.client.post(DRILLS_URL, payload)

        # Assert that the drill was created successfully
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Fetch the created drill from the database
        drill = Drill.objects.get(id=res.data['id'])

        # Assert that the uploadedBy field is correctly set to the authenticated user
        self.assertEqual(drill.uploadedBy, self.user)

    def test_partial_update(self):
        """Test updating a drillScore with patch"""
        user = create_user(
            email='unique_user@example.com',
            password='testpass123',
        )

        self.client.force_authenticate(user)

        drillPayload = prepare_drill_payload()

        drill = create_drill(drillPayload)

        payload = {
            'name': 'Updated Drill Name',
        }
        url = detail_url(drill.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        drill.refresh_from_db()
        self.assertEqual(drill.name, 'Updated Drill Name')
        self.assertEqual(drill.maxScore, 10)
        self.assertEqual(drill.type, 'standard')

    def test_full_update(self):
        """Test updating a drill with put"""
        user = create_user(
            email='user4321@example.com',
            password='pass4321',
        )

        self.client.force_authenticate(user)

        drillPayload = prepare_drill_payload()

        drill = create_drill(drillPayload)

        skill_names = ['draw', 'position', 'shape']

        skills = [Skill.objects.get_or_create(name=name)[0] for name in skill_names]

        payload = {
            'name': 'Updated Drill Name',
            'maxScore': 15,
            'instructions': 'Updated instructions',
            'type': 'highscore',
            'skills': [skill.id for skill in skills],
        }

        url = detail_url(drill.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        drill.refresh_from_db()
        for k, v in payload.items():
            if k == 'skills':
                # Convert JSON string back to list for comparison
                self.assertEqual(json.loads(v), getattr(drill, k))
            else:
                self.assertEqual(v, getattr(drill, k))

    def test_update_user_returns_error(self):
        """Test changing the drill user results in an error."""
        user = create_user(
            email='user4321@example.com',
            password='pass4321',
        )

        self.client.force_authenticate(user)

        drillPayload = prepare_drill_payload()

        drill = create_drill(drillPayload)

        user2 = create_user(
            email='user43212@example.com',
            password='pass4321',
        )

        payload = {
            'uploadedBy': user2,
        }

        url = detail_url(drill.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        drill.refresh_from_db()
        self.assertEqual(drill.uploadedBy, user)

    def test_delete_drill(self):
        """Test deleting a drill"""
        user = create_user(
            email='user4321@example.com',
            password='pass4321',
        )

        self.client.force_authenticate(user)

        skill_names = ['draw', 'position', 'shape']

        skills = [Skill.objects.get_or_create(name=name)[0] for name in skill_names]

        drill = create_drill(
            uploadedBy=user,
            name='Drill 1',
            maxScore=10,
            instructions='Test instructions',
            type='standard',
            skills=[skill.id for skill in skills],
        )

        url = detail_url(drill.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Drill.objects.filter(id=drill.id).exists())
