"""
Tests for drillset APIs.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import DrillSet, Drill, DrillSetMembership

import random
import string

from drillset.serializers import (
    DrillSetSerializer,
    DrillSetDetailSerializer
)

DRILLSET_URL = reverse('drillset:drillset-list')


def detail_url(drillSetId):
    """Return drillset detail URL"""
    return reverse('drillset:drillset-detail', args=[drillSetId])


def create_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)


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

    drill_set = DrillSet.objects.create(
        name="Example Drill Set",
        createdBy=createdBy
    )

    DrillSetMembership.objects.create(
        drill=drill1, drill_set=drill_set, position=1)
    DrillSetMembership.objects.create(
        drill=drill2, drill_set=drill_set, position=2)

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
        DrillSet.objects.create(
            name='Routine 1',
            createdBy=create_user(
                email='user1@example.com',
                password='pass123'
            )
        )
        DrillSet.objects.create(
            name='Routine 2',
            createdBy=create_user(
                email='user2@example.com',
                password='pass123'
            )
        )

        res = self.client.get(DRILLSET_URL)
        drillsets = DrillSet.objects.all().order_by('-id')
        serializer = DrillSetSerializer(drillsets, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PrivateDrillSetApiTests(TestCase):
    """Test the authorized user drillsets API"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_simple_drillset_creation(self):
        """Simple test for creating a drillset with a single drill"""
        drill = create_drill(createdBy=self.user)

        drill_set = DrillSet.objects.create(
            name='Simple Routine', createdBy=self.user)
        DrillSetMembership.objects.create(
            drill=drill, drill_set=drill_set, position=1)

        memberships = DrillSetMembership.objects.filter(drill_set=drill_set)
        drills_via_membership = [
            membership.drill for membership in memberships]

        self.assertEqual(drills_via_membership, [drill])

    def test_create_drillset(self):
        """Test creating a drillset"""
        drill = create_drill(createdBy=self.user)

        drillset = DrillSet.objects.create(
            name='Routine 1', createdBy=self.user)

        DrillSetMembership.objects.create(
            drill=drill, drill_set=drillset, position=1)

        drillset.refresh_from_db()

        drills_in_set = Drill.objects.filter(
            drillsetmembership__drill_set=drillset
        ).order_by('drillsetmembership__position')

        self.assertEqual(list(drills_in_set), [drill])

    def test_create_drillset2(self):
        """Test creating a drillset with multiple drills"""
        drill = create_drill(createdBy=self.user)
        drill2 = create_drill(createdBy=self.user)
        drill3 = create_drill(createdBy=self.user)

        drillset = DrillSet.objects.create(
            name='Routine 1', createdBy=self.user)

        DrillSetMembership.objects.create(
            drill=drill, drill_set=drillset, position=1)
        DrillSetMembership.objects.create(
            drill=drill2, drill_set=drillset, position=2)
        DrillSetMembership.objects.create(
            drill=drill3, drill_set=drillset, position=3)

        drillset.refresh_from_db()

        drills_in_set = Drill.objects.filter(
            drillsetmembership__drill_set=drillset
        ).order_by('drillsetmembership__position')

        self.assertEqual(list(drills_in_set), [drill, drill2, drill3])

    def test_create_drillset_with_payload(self):
        """Test creating a drillset with a payload"""
        drill1 = create_drill(createdBy=self.user)
        drill2 = create_drill(createdBy=self.user)

        payload = {
            'name': 'Routine 1',
            'drills': [drill1.id, drill2.id]
        }

        res = self.client.post(DRILLSET_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        drillset = DrillSet.objects.get(id=res.data['id'])
        drills_in_set = Drill.objects.filter(
            drillsetmembership__drill_set=drillset
        ).order_by('drillsetmembership__position')

        # Assert the correct drills are in the set
        self.assertEqual(list(drills_in_set), [drill1, drill2])

    def test_partial_update_drillset(self):
        """Test partially updating a drillset with patch"""
        drillset = DrillSet.objects.create(
            name='Routine 1',
            createdBy=self.user
        )
        new_drill = create_drill(createdBy=self.user)
        DrillSetMembership.objects.create(
            drill=new_drill, drill_set=drillset, position=1)

        payload = {'name': 'Updated Routine', 'drills': [new_drill.id]}

        url = detail_url(drillset.id)
        res = self.client.patch(url, payload)

        drillset.refresh_from_db()
        memberships = DrillSetMembership.objects.filter(
            drill_set=drillset).order_by('position')
        drills_in_set = [membership.drill for membership in memberships]

        self.assertEqual(drillset.name, payload['name'])
        self.assertEqual(drills_in_set, [new_drill])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_full_update_drillset(self):
        """Test fully updating a drillset with put"""
        drillset = DrillSet.objects.create(
            name='Routine 1',
            createdBy=self.user
        )
        new_drill = create_drill(createdBy=self.user)
        DrillSetMembership.objects.create(
            drill=new_drill, drill_set=drillset, position=1)

        payload = {'name': 'Updated Routine', 'drills': [new_drill.id]}

        url = detail_url(drillset.id)
        res = self.client.put(url, payload)

        drillset.refresh_from_db()
        memberships = DrillSetMembership.objects.filter(
            drill_set=drillset
        ).order_by('position')
        drills_in_set = [membership.drill for membership in memberships]

        self.assertEqual(drillset.name, payload['name'])
        self.assertEqual(drills_in_set, [new_drill])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_drillset(self):
        """Test deleting a drillset"""
        drillset = DrillSet.objects.create(
            name='Routine 1',
            createdBy=self.user
        )

        url = detail_url(drillset.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DrillSet.objects.filter(id=drillset.id).exists())

    def test_fetch_single_drill_set(self):
        """Test retrieving a single drill set"""
        drill1 = create_drill(name='Drill 1', createdBy=self.user)
        drill2 = create_drill(name='Drill 2', createdBy=self.user)
        drill_set = create_drillset(createdBy=self.user)

        DrillSetMembership.objects.create(
            drill=drill1,
            drill_set=drill_set,
            position=1
        )
        DrillSetMembership.objects.create(
            drill=drill2,
            drill_set=drill_set,
            position=2
        )

        url = detail_url(drill_set.id)
        res = self.client.get(url)

        drill_set.refresh_from_db()
        serializer = DrillSetDetailSerializer(drill_set)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
