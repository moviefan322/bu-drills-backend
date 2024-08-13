"""
Tests for drillset APIs.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import DrillSet, Drill

from drillset.serializers import DrillSetSerializer 

DRILLSET_URL = reverse('drillset:drillset-list')

def detail_url(drillSetId):
    """Return drillset detail URL"""
    return reverse('drillset:drillset-detail', args=[drillSetId])

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
    
    drill_set = DrillSet.objects.create(
        name="Example Drill Set",
        createdBy=uploadedBy
    )
    drill_set.drills.add(drill1, drill2)
    
    return drill_set  # Return the created drill set


class PublicDrillSetApiTests(TestCase):
    """Test the public drillset API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required for creating a drillset"""
        payload = {'name': 'DrillSet1'}
        res = self.client.post(DRILLSET_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_drillsets(self):
        """Test retrieving a list of drillsets without authentication"""
        DrillSet.objects.create(name='Routine 1', createdBy=create_user(email='user1@example.com', password='pass123'))
        DrillSet.objects.create(name='Routine 2', createdBy=create_user(email='user2@example.com', password='pass123'))

        res = self.client.get(DRILLSET_URL)
        drillsets = DrillSet.objects.all().order_by('-id')
        serializer = DrillSetSerializer(drillsets, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PrivateDrillSetApiTests(TestCase):
    """Test the authorized user drillsets API"""

    def setUp(self):
        self.user = create_user(email='test@example.com', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_drillset(self):
        """Test creating a drillset"""
        drill = create_drill(uploadedBy=self.user)
        payload = {'name': 'Routine 1', 'drills': [drill.id]}
        res = self.client.post(DRILLSET_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        drillset = DrillSet.objects.get(id=res.data['id'])
        self.assertEqual(drillset.name, payload['name'])
        self.assertEqual(list(drillset.drills.all()), [drill])

    def test_partial_update_drillset(self):
        """Test partially updating a drillset with patch"""
        drillset = DrillSet.objects.create(name='Routine 1', createdBy=self.user)
        new_drill = create_drill(uploadedBy=self.user)
        payload = {'name': 'Updated Routine', 'drills': [new_drill.id]}

        url = detail_url(drillset.id)
        res = self.client.patch(url, payload)

        drillset.refresh_from_db()
        self.assertEqual(drillset.name, payload['name'])
        self.assertEqual(list(drillset.drills.all()), [new_drill])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_full_update_drillset(self):
        """Test fully updating a drillset with put"""
        drillset = DrillSet.objects.create(name='Routine 1', createdBy=self.user)
        new_drill = create_drill(uploadedBy=self.user)
        payload = {'name': 'Updated Routine', 'drills': [new_drill.id]}

        url = detail_url(drillset.id)
        res = self.client.put(url, payload)

        drillset.refresh_from_db()
        self.assertEqual(drillset.name, payload['name'])
        self.assertEqual(list(drillset.drills.all()), [new_drill])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_drillset(self):
        """Test deleting a drillset"""
        drillset = DrillSet.objects.create(name='Routine 1', createdBy=self.user)

        url = detail_url(drillset.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DrillSet.objects.filter(id=drillset.id).exists())
