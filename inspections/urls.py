"""
URL routing for the inspections app.

This module defines the URL patterns for all inspection-related API endpoints.
"""

from django.urls import path
from .views import InspectionListCreateView, InspectionDetailView

app_name = 'inspections'

urlpatterns = [
    # List all inspections and create new ones
    # GET /api/inspections - List all inspections
    # POST /api/inspections - Create a new inspection
    path('inspections', InspectionListCreateView.as_view(), name='inspection-list-create'),
    
    # Retrieve, update, or delete a specific inspection
    # GET /api/inspections/{id} - Retrieve an inspection
    # PUT /api/inspections/{id} - Update an inspection (full)
    # PATCH /api/inspections/{id} - Update an inspection (partial)
    # DELETE /api/inspections/{id} - Delete an inspection
    path('inspections/<int:pk>', InspectionDetailView.as_view(), name='inspection-detail'),
]
