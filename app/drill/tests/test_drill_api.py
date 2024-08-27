"""
Tests for drill APIs.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Drill, TableSetup

import json
import random
import string

from drill.serializers import DrillSerializer, DrillDetailSerializer

DRILLS_URL = reverse('drill:drill-list')
TABLESETUP_URL = reverse('drill:tablesetup-list')


def detail_url(drillId):
    """Return drill detail URL"""
    return reverse('drill:drill-detail', args=[drillId])


def tablesetup_detail_url(tablesetupId):
    """Return table setup detail URL"""
    return reverse('drill:tablesetup-detail', args=[tablesetupId])


def random_string(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def create_drill(createdBy, **params):
    """Create and return a sample drill"""
    defaults = {
        'name': random_string(),
        'maxScore': 10,
        'instructions': 'Suck me off',
        'type': 'standard',
        'skills': ['potting', 'position', 'aim'],
    }
    defaults.update(params)

    drill = Drill.objects.create(createdBy=createdBy, **defaults)
    return drill


def create_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)


class PublicDrillScoreApiTests(TestCase):
    """Test the drill API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required for creating a drill"""
        payload = {
            'name': 'Drill 1',
            'maxScore': 10,
            'instructions': 'Test instructions',
            'type': 'standard',
            'skills': ['potting', 'position', 'aim'],
        }

        res = self.client.post(DRILLS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_drills(self):
        """Test retrieving a list of drillScores."""
        create_drill(createdBy=create_user(email='example@example.com'))
        create_drill(createdBy=create_user(email='example2@example.com'))

        res = self.client.get(DRILLS_URL)

        drillScores = Drill.objects.all().order_by('-id')
        serializer = DrillSerializer(drillScores, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_drill_detail(self):
        """Test viewing a drill detail"""
        drill = create_drill(createdBy=create_user(
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

    def test_create_drill_authenticated(self):
        """Test creating a drill with authentication"""
        payload = {
            'name': 'Drill 1',
            'maxScore': 10,
            'instructions': 'Test instructions',
            'type': 'standard',
            'skills': json.dumps(
                ['potting', 'position', 'aim']
            ),
        }

        res = self.client.post(DRILLS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_drill(self):
        """Test creating a new drill"""
        payload = {
            'name': 'Drill 1',
            'maxScore': 10,
            'instructions': 'Test instructions',
            'type': 'standard',
            'skills': json.dumps(['potting', 'position', 'aim']),
        }
        res = self.client.post(DRILLS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        drill = Drill.objects.get(id=res.data['id'])
        for k, v in payload.items():
            if k == 'skills':
                # Convert JSON string back to list for comparison
                self.assertEqual(json.loads(v), getattr(drill, k))
            else:
                self.assertEqual(v, getattr(drill, k))
        self.assertEqual(drill.createdBy, self.user)

    def test_update_drill_not_owned(self):
        """Test that trying to update a drill not owned by the user fails"""
        other_user = create_user(
            email='other@example.com',
            password='password123',
        )
        drill = create_drill(createdBy=other_user)

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
        drill = create_drill(createdBy=other_user)

        url = detail_url(drill.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Drill.objects.filter(id=drill.id).exists())

    def test_createdBy_is_set_automatically(self):
        """
        Test that createdBy is automatically set to the authenticated user
        """
        payload = {
            'name': 'Drill 1',
            'maxScore': 10,
            'instructions': 'Test instructions',
            'type': 'standard',
            'skills': json.dumps(['potting', 'position', 'aim']),
        }

        res = self.client.post(DRILLS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        drill = Drill.objects.get(id=res.data['id'])
        self.assertEqual(drill.createdBy, self.user)

    def test_partial_update(self):
        """Test updating a drillScore with patch"""
        user = create_user(
            email='unique_user@example.com',
            password='testpass123',
        )

        self.client.force_authenticate(user)

        drill = create_drill(
            createdBy=user,
            name='Drill 1',
            maxScore=10,
            instructions='Test instructions',
            type='standard',
            skills=json.dumps(['potting', 'position', 'aim']),
        )

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

        drill = create_drill(
            createdBy=user,
            name='Drill 1',
            maxScore=10,
            instructions='Test instructions',
            type='standard',
            skills=json.dumps(['potting', 'position', 'aim']),
        )

        payload = {
            'name': 'Updated Drill Name',
            'maxScore': 15,
            'instructions': 'Updated instructions',
            'type': 'highscore',
            'skills': json.dumps(['potting', 'position', 'aim', 'break']),
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

        drill = create_drill(
            createdBy=user,
            name='Drill 1',
            maxScore=10,
            instructions='Test instructions',
            type='standard',
            skills=json.dumps(['potting', 'position', 'aim']),
        )

        user2 = create_user(
            email='user43212@example.com',
            password='pass4321',
        )

        payload = {
            'createdBy': user2,
        }

        url = detail_url(drill.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        drill.refresh_from_db()
        self.assertEqual(drill.createdBy, user)

    def test_delete_drill(self):
        """Test deleting a drill"""
        user = create_user(
            email='user4321@example.com',
            password='pass4321',
        )

        self.client.force_authenticate(user)

        drill = create_drill(
            createdBy=user,
            name='Drill 1',
            maxScore=10,
            instructions='Test instructions',
            type='standard',
            skills=json.dumps(['potting', 'position', 'aim']),
        )

        url = detail_url(drill.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Drill.objects.filter(id=drill.id).exists())


class PrivateTableSetupApiTests(TestCase):
    """Test the authorized user TableSetup API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_create_tablesetup(self):
        """Test creating a TableSetup for a drill"""
        drill = create_drill(createdBy=self.user)
        payload = {
            'drill': drill.id,
            'drillName': drill.name,
            'ballPositionProps': [{'x': 0.5, 'y': 0.5, 'number': 1}],
            'pottingPocketProp': [{'x': 0.3, 'y': 0.3, 'show': True}],
            'targetSpecs': [{
                'isTarget': True,
                'x': 0.4,
                'y': 0.7,
                'rotate': False, 'w': 1.0, 'h': 0.5
            }],
            'leaveLineProp': [{'draw': True, 'x': 0.6, 'y': 0.4}],
            'kickShotLineProp': [{'draw': True, 'rails': 2, 'objectBall': 3}],
            'bankShotLineProp': {
                'draw': True,
                'objectBall': 1,
                'pocket': {'x': 0.1, 'y': 0.1}
            },
            'startIndex': 0,
            'showShotLine': True,
        }

        res = self.client.post(TABLESETUP_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tablesetup = TableSetup.objects.get(id=res.data['id'])
        self.assertEqual(tablesetup.drill, drill)
        self.assertEqual(tablesetup.startIndex, payload['startIndex'])
        self.assertTrue(tablesetup.showShotLine)
        self.assertEqual(tablesetup.ballPositionProps,
                         payload['ballPositionProps'])

    def test_retrieve_tablesetup(self):
        """Test retrieving a list of TableSetups"""
        drill = create_drill(createdBy=self.user)
        tablesetup = TableSetup.objects.create(
            drill=drill,
            drillName=drill.name,
            ballPositionProps=[{'x': 0.5, 'y': 0.5, 'number': 1}],
            pottingPocketProp=[{'x': 0.3, 'y': 0.3, 'show': True}],
            targetSpecs=[{'isTarget': True, 'x': 0.4, 'y': 0.7,
                          'rotate': False, 'w': 1.0, 'h': 0.5}],
            leaveLineProp=[{'draw': True, 'x': 0.6, 'y': 0.4}],
            kickShotLineProp=[{'draw': True, 'rails': 2, 'objectBall': 3}],
            bankShotLineProp={'draw': True, 'objectBall': 1,
                              'pocket': {'x': 0.1, 'y': 0.1}},
            startIndex=0,
            showShotLine=True,
        )

        url = tablesetup_detail_url(tablesetup.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], tablesetup.id)

    def test_partial_update_tablesetup(self):
        """Test updating a TableSetup with patch"""
        drill = create_drill(createdBy=self.user)
        tablesetup = TableSetup.objects.create(
            drill=drill,
            ballPositionProps=[{'x': 0.5, 'y': 0.5, 'number': 1}],
            pottingPocketProp=[{'x': 0.3, 'y': 0.3, 'show': True}],
            targetSpecs=[{'isTarget': True, 'x': 0.4, 'y': 0.7,
                          'rotate': False, 'w': 1.0, 'h': 0.5}],
            leaveLineProp=[{'draw': True, 'x': 0.6, 'y': 0.4}],
            kickShotLineProp=[{'draw': True, 'rails': 2, 'objectBall': 3}],
            bankShotLineProp={'draw': True, 'objectBall': 1,
                              'pocket': {'x': 0.1, 'y': 0.1}},
            startIndex=0,
            showShotLine=True,
        )

        payload = {'startIndex': 1}
        url = tablesetup_detail_url(tablesetup.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tablesetup.refresh_from_db()
        self.assertEqual(tablesetup.startIndex, payload['startIndex'])

    def test_full_update_tablesetup(self):
        """Test updating a TableSetup with put"""
        drill = create_drill(createdBy=self.user)
        tablesetup = TableSetup.objects.create(
            drill=drill,
            drillName=drill.name,
            ballPositionProps=[{'x': 0.5, 'y': 0.5, 'number': 1}],
            pottingPocketProp=[{'x': 0.3, 'y': 0.3, 'show': True}],
            targetSpecs=[{'isTarget': True, 'x': 0.4, 'y': 0.7,
                          'rotate': False, 'w': 1.0, 'h': 0.5}],
            leaveLineProp=[{'draw': True, 'x': 0.6, 'y': 0.4}],
            kickShotLineProp=[{'draw': True, 'rails': 2, 'objectBall': 3}],
            bankShotLineProp={'draw': True, 'objectBall': 1,
                              'pocket': {'x': 0.1, 'y': 0.1}},
            startIndex=0,
            showShotLine=True,
        )

        payload = {
            'drill': drill.id,
            'drillName': drill.name + '2',
            'ballPositionProps': [{'x': 0.6, 'y': 0.4, 'number': 2}],
            'pottingPocketProp': [{'x': 0.4, 'y': 0.4, 'show': False}],
            'targetSpecs': [{
                'isTarget': False,
                'x': 0.5, 'y': 0.8,
                'rotate': True, 'w': 1.5, 'h': 0.7
            }],
            'leaveLineProp': [{'draw': False, 'x': 0.7, 'y': 0.5}],
            'kickShotLineProp': [{'draw': False, 'rails': 3, 'objectBall': 4}],
            'bankShotLineProp': {
                'draw': False,
                'objectBall': 2,
                'pocket': {'x': 0.2, 'y': 0.2}
            },
            'startIndex': 2,
            'showShotLine': False,
        }

        url = tablesetup_detail_url(tablesetup.id)
        res = self.client.put(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tablesetup.refresh_from_db()
        self.assertEqual(tablesetup.startIndex, payload['startIndex'])
        self.assertFalse(tablesetup.showShotLine)
        self.assertEqual(tablesetup.ballPositionProps,
                         payload['ballPositionProps'])

    def test_delete_tablesetup(self):
        """Test deleting a TableSetup"""
        drill = create_drill(createdBy=self.user)
        tablesetup = TableSetup.objects.create(
            drill=drill,
            ballPositionProps=[{'x': 0.5, 'y': 0.5, 'number': 1}],
            pottingPocketProp=[{'x': 0.3, 'y': 0.3, 'show': True}],
            targetSpecs=[{
                'isTarget': True,
                'x': 0.4,
                'y': 0.7,
                'rotate': False, 'w': 1.0, 'h': 0.5
            }],
            leaveLineProp=[{'draw': True, 'x': 0.6, 'y': 0.4}],
            kickShotLineProp=[{'draw': True, 'rails': 2, 'objectBall': 3}],
            bankShotLineProp={
                'draw': True,
                'objectBall': 1,
                'pocket': {'x': 0.1, 'y': 0.1}
            },
            startIndex=0,
            showShotLine=True,
        )

        url = tablesetup_detail_url(tablesetup.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TableSetup.objects.filter(id=tablesetup.id).exists())

    def test_create_drill_with_tablesetup(self):
        """Test creating a drill and linking it to a TableSetup"""
        # Create a drill
        drill = create_drill(createdBy=self.user)

        # Create a tablesetup and link it to the drill
        tablesetup = TableSetup.objects.create(
            drill=drill,
            ballPositionProps=[{'x': 0.5, 'y': 0.5, 'number': 1}],
            pottingPocketProp=[{'x': 0.3, 'y': 0.3, 'show': True}],
            targetSpecs=[{
                'isTarget': True,
                'x': 0.4, 'y': 0.7,
                'rotate': False, 'w': 1.0, 'h': 0.5}],
            leaveLineProp=[{'draw': True, 'x': 0.6, 'y': 0.4}],
            kickShotLineProp=[{'draw': True, 'rails': 2, 'objectBall': 3}],
            bankShotLineProp={
                'draw': True,
                'objectBall': 1,
                'pocket': {'x': 0.1, 'y': 0.1}},
            startIndex=0,
            showShotLine=True,
        )

        # Explicitly set the tableSetup field on the drill
        drill.tableSetup = tablesetup
        drill.save()

        # Fetch the drill from the database
        drill.refresh_from_db()

        # Check if the drill's tableSetup field is correctly set
        self.assertIsNotNone(drill.tableSetup)
        self.assertEqual(drill.tableSetup.id, tablesetup.id)

        # Fetch the drill via the API and check the tableSetup field
        url = detail_url(drill.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['tableSetup']['id'], tablesetup.id)

    def test_create_drill_with_tablesetup2(self):
        """Test creating a drill and linking it to a TableSetup"""
        # Create a drill
        drill = create_drill(createdBy=self.user)

        # Create a tablesetup and link it to the drill
        tablesetup = TableSetup.objects.create(
            drill=drill,
            ballPositionProps=[{'x': 0.5, 'y': 0.5, 'number': 1}],
            pottingPocketProp=[{'x': 0.3, 'y': 0.3, 'show': True}],
            targetSpecs=[{
                'isTarget': True,
                'x': 0.4,
                'y': 0.7,
                'rotate': False, 'w': 1.0, 'h': 0.5}
            ],
            leaveLineProp=[{'draw': True, 'x': 0.6, 'y': 0.4}],
            kickShotLineProp=[{'draw': True, 'rails': 2, 'objectBall': 3}],
            bankShotLineProp={
                'draw': True,
                'objectBall': 1,
                'pocket': {'x': 0.1, 'y': 0.1}
            },
            startIndex=0,
            showShotLine=True,
        )

        # Fetch the drill from the database
        drill.refresh_from_db()

        # Check if the drill's tableSetup field is correctly set
        self.assertIsNotNone(drill.tableSetup)
        self.assertEqual(drill.tableSetup.id, tablesetup.id)

        # Fetch the drill via the API and check the tableSetup field
        url = detail_url(drill.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['tableSetup']['id'], tablesetup.id)
