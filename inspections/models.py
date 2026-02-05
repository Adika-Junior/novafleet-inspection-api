"""
Data models for the NovaFleet Inspection system.

This module defines the Inspection model which represents a vehicle inspection
with validation rules for dates and status values, plus InspectionHistory for tracking changes.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User


class Inspection(models.Model):
    """
    Represents a vehicle inspection record.
    
    Attributes:
        vehicle_plate (str): The vehicle's license plate number (e.g., "ABC-1234")
        inspection_date (date): The scheduled or completed inspection date
        status (str): Current status - must be "scheduled", "passed", or "failed"
        notes (str): Optional notes about the inspection
        created_at (datetime): Timestamp when the record was created
        updated_at (datetime): Timestamp when the record was last updated
    
    Business Rules:
        - inspection_date cannot be in the past
        - status must be one of the predefined STATUS_CHOICES
        - vehicle_plate is required
    """
    
    # Status choices as constants for type safety and maintainability
    STATUS_SCHEDULED = 'scheduled'
    STATUS_PASSED = 'passed'
    STATUS_FAILED = 'failed'
    
    STATUS_CHOICES = [
        (STATUS_SCHEDULED, 'Scheduled'),
        (STATUS_PASSED, 'Passed'),
        (STATUS_FAILED, 'Failed'),
    ]
    
    # Core fields
    vehicle_plate = models.CharField(
        max_length=20,
        help_text="Vehicle license plate number (e.g., ABC-1234)"
    )
    
    inspection_date = models.DateField(
        help_text="Date of the inspection (cannot be in the past)"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SCHEDULED,
        help_text="Current status of the inspection"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Optional notes about the inspection"
    )
    
    # Audit fields
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the inspection was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the inspection was last updated"
    )
    
    class Meta:
        """Model metadata configuration."""
        ordering = ['-inspection_date', '-created_at']
        verbose_name = 'Inspection'
        verbose_name_plural = 'Inspections'
        indexes = [
            models.Index(fields=['vehicle_plate']),
            models.Index(fields=['inspection_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        """String representation of the inspection."""
        return f"{self.vehicle_plate} - {self.inspection_date} ({self.get_status_display()})"
    
    def clean(self):
        """
        Validate the model data before saving.
        
        Raises:
            ValidationError: If inspection_date is in the past
        """
        super().clean()
        
        # Validate that inspection date is not in the past
        if self.inspection_date:
            today = timezone.now().date()
            if self.inspection_date < today:
                raise ValidationError({
                    'inspection_date': 'Inspection date cannot be in the past.'
                })
    
    def save(self, *args, **kwargs):
        """
        Override save method to ensure validation is always run and track history.
        
        This ensures that business rules are enforced even when
        objects are created programmatically.
        """
        # Store old status for history tracking
        old_status = None
        if self.pk:
            try:
                old_instance = Inspection.objects.get(pk=self.pk)
                old_status = old_instance.status
            except Inspection.DoesNotExist:
                pass
        
        self.full_clean()
        super().save(*args, **kwargs)
        
        # Create history record if status changed
        if old_status and old_status != self.status:
            InspectionHistory.objects.create(
                inspection=self,
                old_status=old_status,
                new_status=self.status,
                changed_at=timezone.now(),
                notes=f"Status changed from {old_status} to {self.status}"
            )


class InspectionHistory(models.Model):
    """
    Tracks the history of changes to inspections.
    
    This model maintains an audit trail of all status changes
    for compliance and tracking purposes.
    """
    
    inspection = models.ForeignKey(
        Inspection,
        on_delete=models.CASCADE,
        related_name='history',
        help_text="The inspection this history record belongs to"
    )
    
    old_status = models.CharField(
        max_length=20,
        choices=Inspection.STATUS_CHOICES,
        help_text="Previous status before the change"
    )
    
    new_status = models.CharField(
        max_length=20,
        choices=Inspection.STATUS_CHOICES,
        help_text="New status after the change"
    )
    
    changed_at = models.DateTimeField(
        help_text="When the status change occurred"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Optional notes about the change"
    )
    
    class Meta:
        """Model metadata configuration."""
        ordering = ['-changed_at']
        verbose_name = 'Inspection History'
        verbose_name_plural = 'Inspection Histories'
        indexes = [
            models.Index(fields=['inspection', '-changed_at']),
        ]
    
    def __str__(self):
        """String representation of the history record."""
        return f"{self.inspection.vehicle_plate}: {self.old_status} → {self.new_status} at {self.changed_at}"