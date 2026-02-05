"""
Django app configuration for the inspections module.
"""

from django.apps import AppConfig


class InspectionsConfig(AppConfig):
    """Configuration class for the inspections application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inspections'
    verbose_name = 'Vehicle Inspections'
