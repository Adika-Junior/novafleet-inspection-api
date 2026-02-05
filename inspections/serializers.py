"""
Django REST Framework serializers for the inspections app.

Serializers handle the conversion between complex data types (like Django models)
and Python datatypes that can be easily rendered into JSON.
"""

from rest_framework import serializers
from django.utils import timezone
from .models import Inspection


class InspectionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Inspection model.
    
    This serializer handles:
    - Conversion between Inspection model instances and JSON
    - Validation of input data according to business rules
    - Custom error messages for better API usability
    
    Validation Rules:
        - inspection_date: Cannot be in the past
        - status: Must be one of "scheduled", "passed", or "failed"
        - vehicle_plate: Required field
    """
    
    class Meta:
        model = Inspection
        fields = [
            'id',
            'vehicle_plate',
            'inspection_date',
            'status',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_inspection_date(self, value):
        """
        Validate inspection date based on inspection status.
        
        Business Rules:
        - For "scheduled" inspections: Date must be in the future
        - For "passed" or "failed" inspections: Date can be in past (recording historical inspections)
        
        Args:
            value (date): The inspection date to validate
            
        Returns:
            date: The validated date
            
        Raises:
            serializers.ValidationError: If validation rules are violated
        """
        today = timezone.now().date()
        
        # Get the status from the request data or existing instance
        status = self.initial_data.get('status')
        if status is None and self.instance:
            status = self.instance.status
        
        # Only enforce future-date requirement for scheduled inspections
        if value < today and status == Inspection.STATUS_SCHEDULED:
            raise serializers.ValidationError(
                f"Inspections scheduled for a past date are not allowed. "
                f"Today is {today.isoformat()}, but received {value.isoformat()}. "
                f"Note: You can record a historic inspection by using status 'passed' or 'failed'."
            )
        
        return value
    
    def validate_status(self, value):
        """
        Validate that the status is one of the allowed values.
        
        Args:
            value (str): The status to validate
            
        Returns:
            str: The validated status
            
        Raises:
            serializers.ValidationError: If the status is invalid
        """
        valid_statuses = [choice[0] for choice in Inspection.STATUS_CHOICES]
        
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f'Invalid status "{value}". '
                f'Status must be one of: {", ".join(valid_statuses)}.'
            )
        
        return value
    
    def validate_vehicle_plate(self, value):
        """
        Validate and normalize the vehicle plate.
        
        Args:
            value (str): The vehicle plate to validate
            
        Returns:
            str: The validated and normalized vehicle plate
            
        Raises:
            serializers.ValidationError: If the plate is invalid
        """
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Vehicle plate cannot be empty."
            )
        
        # Normalize: strip whitespace and convert to uppercase
        return value.strip().upper()
    
    def to_representation(self, instance):
        """
        Customize the output representation of the serializer.
        
        This method formats the response data for better readability.
        
        Args:
            instance (Inspection): The inspection instance to serialize
            
        Returns:
            dict: The serialized representation
        """
        representation = super().to_representation(instance)
        
        # Format dates in ISO format for consistency
        if representation.get('inspection_date'):
            representation['inspection_date'] = instance.inspection_date.isoformat()
        
        return representation
