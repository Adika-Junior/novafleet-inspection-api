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
