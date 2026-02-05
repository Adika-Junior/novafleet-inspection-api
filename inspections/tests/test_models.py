"""
Unit tests for the Inspection model.

This module tests the model's validation logic and business rules.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from inspections.models import Inspection


class InspectionModelTest(TestCase):
    """Test cases for the Inspection model."""
    
    def setUp(self):
        """Set up test data that will be used across multiple tests."""
        self.valid_data = {
            'vehicle_plate': 'ABC-1234',
            'inspection_date': date.today() + timedelta(days=1),
            'status': Inspection.STATUS_SCHEDULED,
            'notes': 'Regular inspection'
        }
    
    def test_create_valid_inspection(self):
        """Test creating an inspection with valid data."""
        inspection = Inspection.objects.create(**self.valid_data)
        
        self.assertEqual(inspection.vehicle_plate, 'ABC-1234')
        self.assertEqual(inspection.status, Inspection.STATUS_SCHEDULED)
        self.assertIsNotNone(inspection.created_at)
        self.assertIsNotNone(inspection.updated_at)
    
    def test_inspection_date_in_past_raises_error(self):
        """Test that creating an inspection with a past date raises ValidationError."""
        past_date = date.today() - timedelta(days=1)
        
        with self.assertRaises(ValidationError) as context:
            inspection = Inspection(
                vehicle_plate='XYZ-5678',
                inspection_date=past_date,
                status=Inspection.STATUS_SCHEDULED
            )
            inspection.save()
        
        self.assertIn('inspection_date', str(context.exception))
    
    def test_inspection_string_representation(self):
        """Test the string representation of an inspection."""
        inspection = Inspection.objects.create(**self.valid_data)
        expected = f"ABC-1234 - {self.valid_data['inspection_date']} (Scheduled)"
        
        self.assertEqual(str(inspection), expected)
    
    def test_status_choices(self):
        """Test that all status choices are valid."""
        for status_value, _ in Inspection.STATUS_CHOICES:
            inspection = Inspection.objects.create(
                vehicle_plate='TEST-001',
                inspection_date=date.today() + timedelta(days=1),
                status=status_value
            )
            self.assertEqual(inspection.status, status_value)
    
    def test_notes_optional(self):
        """Test that notes field is optional."""
        data = self.valid_data.copy()
        data.pop('notes')
        
        inspection = Inspection.objects.create(**data)
        self.assertIsNone(inspection.notes)
