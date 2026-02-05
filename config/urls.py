"""
URL Configuration for NovaFleet Inspection API

This module defines the main URL routing for the project, including:
- API endpoints for inspections
- Swagger/OpenAPI documentation
- Django admin interface
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="NovaFleet Inspection API",
        default_version='v1',
        description="""
        # NovaFleet Vehicle Inspection Tracker API
        
        This API allows you to manage vehicle inspections for the NovaFleet system.
        
        ## Features
        - Create new vehicle inspections
        - Retrieve all inspections or a specific inspection
        - Update inspection status (scheduled, passed, failed)
        - Automatic validation of inspection dates and status values
        
        ## Business Rules
        - Inspection dates cannot be in the past
        - Status must be one of: "scheduled", "passed", or "failed"
        - Vehicle plate is required for all inspections
        
        ## Getting Started
        Use the endpoints below to interact with the inspection system.
        All endpoints return JSON responses.
        """,
        terms_of_service="https://www.novafleet.com/terms/",
        contact=openapi.Contact(email="julius@trinovaltd.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Root redirect to API documentation
    path('', RedirectView.as_view(url='/swagger/', permanent=False), name='root-redirect'),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('inspections.urls')),
    
    # Swagger UI - Interactive API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # ReDoc - Alternative API documentation
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # OpenAPI JSON schema
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
