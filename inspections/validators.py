"""
Custom validators for the inspections app.

This module contains reusable validation functions that enforce
business rules for inspection data.
"""

from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date


def validate_inspection_date(value):
    """
    Validate that an inspection date is not in the past.
    
    Args:
        value (date): The inspection date to validate
        
    Raises:
        ValidationError: If the date is in the past
        
    Example:
        >>> from datetime import date, timedelta
        >>> future_date = date.today() + timedelta(days=1)
        >>> validate_inspection_date(future_date)  # No error
        >>> past_date = date.today() - timedelta(days=1)
        >>> validate_inspection_date(past_date)  # Raises ValidationError
    """
    if not isinstance(value, date):
        raise ValidationError('Invalid date format.')
    
    today = timezone.now().date()
    if value < today:
        raise ValidationError(
            'Inspection date cannot be in the past. '
            f'Today is {today.isoformat()}, but received {value.isoformat()}.'
        )


def validate_status(value):
    """
    Validate that a status value is one of the allowed choices.
    
    Args:
        value (str): The status value to validate
        
    Raises:
        ValidationError: If the status is not valid
        
    Example:
        >>> validate_status('scheduled')  # No error
        >>> validate_status('invalid')  # Raises ValidationError
    """
    valid_statuses = ['scheduled', 'passed', 'failed']
    
    if value not in valid_statuses:
        raise ValidationError(
            f'Invalid status "{value}". '
            f'Status must be one of: {", ".join(valid_statuses)}.'
        )
