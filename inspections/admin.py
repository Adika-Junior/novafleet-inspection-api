"""
Django admin configuration for the inspections app.

This module customizes the Django admin interface for managing inspections.
"""

from django.contrib import admin
from .models import Inspection


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Inspection model.
    
    Features:
    - List display with key fields
    - Filtering by status and date
    - Search by vehicle plate
    - Read-only audit fields
    """
    
    list_display = [
        'id',
        'vehicle_plate',
        'inspection_date',
        'status',
        'created_at',
        'updated_at'
    ]
    
    list_filter = [
        'status',
        'inspection_date',
        'created_at'
    ]
    
    search_fields = [
        'vehicle_plate',
        'notes'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at'
    ]
    
    ordering = ['-inspection_date', '-created_at']
    
    fieldsets = (
        ('Inspection Details', {
            'fields': ('vehicle_plate', 'inspection_date', 'status')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Audit Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
