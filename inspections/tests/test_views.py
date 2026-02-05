"""
API endpoint tests for the inspections app.

This module contains the two required tests as specified in the project requirements:
1. Test successful inspection creation with valid data
2. Test that inspections with past dates are rejected
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from inspections.models import Inspection


class InspectionAPITest(TestCase):
    """Test cases for the Inspection API endpoints."""
    
    def setUp(self):
        """Set up test client and common test data."""
        self.client = APIClient()
        self.list_url = reverse('inspections:inspection-list-create')
        
        # Valid inspection data for testing
        self.valid_inspection_data = {
            'vehicle_plate': 'ABC-1234',
            'inspection_date': (date.today() + timedelta(days=7)).isoformat(),
            'status': 'scheduled',
            'notes': 'Regular maintenance inspection'
        }
    
    def test_create_inspection_with_valid_data(self):
        """
        REQUIRED TEST 1: Test successful inspection creation with valid data.
        
        This test verifies that:
        - A POST request with valid data creates an inspection
        - The response status is 201 Created
        - The returned data matches the input
        - The inspection is saved in the database
        """
        response = self.client.post(
            self.list_url,
            self.valid_inspection_data,
            format='json'
        )
        
        # Assert successful creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Assert response contains expected data
        self.assertEqual(response.data['vehicle_plate'], 'ABC-1234')
        self.assertEqual(response.data['status'], 'scheduled')
        self.assertEqual(response.data['notes'], 'Regular maintenance inspection')
        
        # Assert inspection was saved to database
        self.assertEqual(Inspection.objects.count(), 1)
        
        # Assert the saved inspection has correct data
        inspection = Inspection.objects.first()
        self.assertEqual(inspection.vehicle_plate, 'ABC-1234')
        self.assertEqual(inspection.status, 'scheduled')
    
    def test_reject_inspection_with_past_date(self):
        """
        REQUIRED TEST 2: Test that inspections with past dates are rejected.
        
        This test verifies that:
        - A POST request with a past date is rejected
        - The response status is 400 Bad Request
        - An appropriate error message is returned
        - No inspection is created in the database
        """
        # Create inspection data with a past date
        past_date = date.today() - timedelta(days=1)
        invalid_data = {
            'vehicle_plate': 'XYZ-5678',
            'inspection_date': past_date.isoformat(),
            'status': 'scheduled',
            'notes': 'This should fail'
        }
        
        response = self.client.post(
            self.list_url,
            invalid_data,
            format='json'
        )
        
        # Assert request was rejected
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Assert error message mentions inspection_date
        self.assertIn('inspection_date', response.data)
        
        # Assert error message mentions "past"
        error_message = str(response.data['inspection_date'][0]).lower()
        self.assertIn('past', error_message)
        
        # Assert no inspection was created
        self.assertEqual(Inspection.objects.count(), 0)
    
    # Additional tests for comprehensive coverage
    
    def test_list_all_inspections(self):
        """Test retrieving a list of all inspections."""
        # Clear any existing data to ensure clean test
        Inspection.objects.all().delete()
        
        # Verify database is empty
        self.assertEqual(Inspection.objects.count(), 0)
        
        # Create test inspections
        inspection1 = Inspection.objects.create(
            vehicle_plate='TEST-001',
            inspection_date=date.today() + timedelta(days=1),
            status='scheduled'
        )
        inspection2 = Inspection.objects.create(
            vehicle_plate='TEST-002',
            inspection_date=date.today() + timedelta(days=2),
            status='passed'
        )
        
        # Verify we have exactly 2 in database
        self.assertEqual(Inspection.objects.count(), 2)
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # The response is paginated, so check the 'results' key
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
    
    def test_retrieve_single_inspection(self):
        """Test retrieving a specific inspection by ID."""
        inspection = Inspection.objects.create(
            vehicle_plate='TEST-003',
            inspection_date=date.today() + timedelta(days=1),
            status='scheduled'
        )
        
        detail_url = reverse('inspections:inspection-detail', kwargs={'pk': inspection.id})
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vehicle_plate'], 'TEST-003')
    
    def test_update_inspection_status(self):
        """Test updating an inspection's status."""
        inspection = Inspection.objects.create(
            vehicle_plate='TEST-004',
            inspection_date=date.today() + timedelta(days=1),
            status='scheduled'
        )
        
        detail_url = reverse('inspections:inspection-detail', kwargs={'pk': inspection.id})
        update_data = {
            'vehicle_plate': 'TEST-004',
            'inspection_date': (date.today() + timedelta(days=1)).isoformat(),
            'status': 'passed',
            'notes': 'Inspection completed successfully'
        }
        
        response = self.client.put(detail_url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'passed')
        
        # Verify database was updated
        inspection.refresh_from_db()
        self.assertEqual(inspection.status, 'passed')
    
    def test_invalid_status_rejected(self):
        """Test that invalid status values are rejected."""
        invalid_data = self.valid_inspection_data.copy()
        invalid_data['status'] = 'invalid_status'
        
        response = self.client.post(self.list_url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)
    
    def test_missing_required_fields(self):
        """Test that requests with missing required fields are rejected."""
        incomplete_data = {
            'vehicle_plate': 'TEST-005'
            # Missing inspection_date and status
        }
        
        response = self.client.post(self.list_url, incomplete_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_record_historical_passed_inspection(self):
        """Test that we can record a past inspection with status 'passed'."""
        # Create inspection data with a past date but status='passed'
        past_date = date.today() - timedelta(days=5)
        historical_data = {
            'vehicle_plate': 'HIST-001',
            'inspection_date': past_date.isoformat(),
            'status': 'passed',
            'notes': 'Historical inspection record'
        }
        
        response = self.client.post(self.list_url, historical_data, format='json')
        
        # Should succeed because status is 'passed', not 'scheduled'
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'passed')
        self.assertEqual(response.data['vehicle_plate'], 'HIST-001')
        
        # Verify it was saved
        self.assertEqual(Inspection.objects.count(), 1)
        inspection = Inspection.objects.first()
        self.assertEqual(inspection.status, 'passed')
        self.assertEqual(inspection.inspection_date, past_date)
    
    def test_record_historical_failed_inspection(self):
        """Test that we can record a past inspection with status 'failed'."""
        past_date = date.today() - timedelta(days=3)
        historical_data = {
            'vehicle_plate': 'HIST-002',
            'inspection_date': past_date.isoformat(),
            'status': 'failed',
            'notes': 'Failed emissions test'
        }
        
        response = self.client.post(self.list_url, historical_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'failed')


class InspectionRescheduleTest(TestCase):
    """Test cases for the reschedule functionality."""
    
    def setUp(self):
        """Set up test client and create test inspections."""
        self.client = APIClient()
        
        # Create a failed inspection for rescheduling
        self.failed_inspection = Inspection.objects.create(
            vehicle_plate='FAIL-001',
            inspection_date=date.today() + timedelta(days=1),
            status='failed',
            notes='Failed brake inspection'
        )
        
        # Create a passed inspection for rescheduling
        self.passed_inspection = Inspection.objects.create(
            vehicle_plate='PASS-001',
            inspection_date=date.today() + timedelta(days=2),
            status='passed',
            notes='Passed all checks'
        )
        
        # Create a scheduled inspection (should not be reschedulable)
        self.scheduled_inspection = Inspection.objects.create(
            vehicle_plate='SCHED-001',
            inspection_date=date.today() + timedelta(days=7),
            status='scheduled',
            notes='Upcoming inspection'
        )
    
    def test_reschedule_failed_inspection(self):
        """Test rescheduling a failed inspection to a new future date."""
        reschedule_url = reverse(
            'inspections:inspection-reschedule',
            kwargs={'pk': self.failed_inspection.id}
        )
        
        new_date = date.today() + timedelta(days=14)
        reschedule_data = {
            'new_inspection_date': new_date.isoformat(),
            'notes': 'Rescheduled after brake repair completion'
        }
        
        response = self.client.post(reschedule_url, reschedule_data, format='json')
        
        # Should succeed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'scheduled')
        self.assertEqual(response.data['inspection_date'], new_date.isoformat())
        self.assertIn('Rescheduled', response.data['notes'])
        
        # Verify database was updated
        self.failed_inspection.refresh_from_db()
        self.assertEqual(self.failed_inspection.status, 'scheduled')
        self.assertEqual(self.failed_inspection.inspection_date, new_date)
    
    def test_reschedule_passed_inspection(self):
        """Test rescheduling a passed inspection."""
        reschedule_url = reverse(
            'inspections:inspection-reschedule',
            kwargs={'pk': self.passed_inspection.id}
        )
        
        new_date = date.today() + timedelta(days=30)
        reschedule_data = {
            'new_inspection_date': new_date.isoformat(),
            'notes': 'Annual reinspection'
        }
        
        response = self.client.post(reschedule_url, reschedule_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'scheduled')
        self.assertEqual(response.data['inspection_date'], new_date.isoformat())
    
    def test_cannot_reschedule_scheduled_inspection(self):
        """Test that scheduled inspections cannot be rescheduled."""
        reschedule_url = reverse(
            'inspections:inspection-reschedule',
            kwargs={'pk': self.scheduled_inspection.id}
        )
        
        new_date = date.today() + timedelta(days=14)
        reschedule_data = {
            'new_inspection_date': new_date.isoformat(),
            'notes': 'Trying to reschedule scheduled inspection'
        }
        
        response = self.client.post(reschedule_url, reschedule_data, format='json')
        
        # Should fail
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('scheduled', response.data['error'].lower())
    
    def test_reschedule_to_past_date_rejected(self):
        """Test that rescheduling to a past date is rejected."""
        reschedule_url = reverse(
            'inspections:inspection-reschedule',
            kwargs={'pk': self.failed_inspection.id}
        )
        
        past_date = date.today() - timedelta(days=5)
        reschedule_data = {
            'new_inspection_date': past_date.isoformat(),
            'notes': 'Trying to reschedule to past'
        }
        
        response = self.client.post(reschedule_url, reschedule_data, format='json')
        
        # Should fail
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('must be in the future', response.data['error'])
    
    def test_reschedule_without_new_date_rejected(self):
        """Test that reschedule request without new_inspection_date is rejected."""
        reschedule_url = reverse(
            'inspections:inspection-reschedule',
            kwargs={'pk': self.failed_inspection.id}
        )
        
        reschedule_data = {
            'notes': 'Missing new_inspection_date'
        }
        
        response = self.client.post(reschedule_url, reschedule_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_inspection_date', response.data['error'])
    
    def test_reschedule_with_invalid_date_rejected(self):
        """Test that reschedule with invalid date format is rejected."""
        reschedule_url = reverse(
            'inspections:inspection-reschedule',
            kwargs={'pk': self.failed_inspection.id}
        )
        
        reschedule_data = {
            'new_inspection_date': 'INVALID-DATE',
            'notes': 'Invalid date format'
        }
        
        response = self.client.post(reschedule_url, reschedule_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid date format', response.data['error'])
    
    def test_reschedule_history_tracking(self):
        """Test that status change from failed to scheduled is recorded in history."""
        from inspections.models import InspectionHistory
        
        # Clear history first
        InspectionHistory.objects.all().delete()
        
        reschedule_url = reverse(
            'inspections:inspection-reschedule',
            kwargs={'pk': self.failed_inspection.id}
        )
        
        new_date = date.today() + timedelta(days=14)
        reschedule_data = {
            'new_inspection_date': new_date.isoformat()
        }
        
        response = self.client.post(reschedule_url, reschedule_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify history was recorded
        history = InspectionHistory.objects.filter(inspection=self.failed_inspection)
        self.assertTrue(history.exists())
        
        # Get the history record
        history_record = history.first()
        self.assertEqual(history_record.old_status, 'failed')
        self.assertEqual(history_record.new_status, 'scheduled')
