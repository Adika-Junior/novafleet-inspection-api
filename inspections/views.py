"""
API views for the inspections app.

This module defines the REST API endpoints for managing vehicle inspections.
All views use Django REST Framework's generic views for consistency and
maintainability.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Inspection
from .serializers import InspectionSerializer


class InspectionListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing all inspections and creating new ones.
    
    GET /api/inspections
        Returns a list of all inspection records.
        
        Response: 200 OK
        [
            {
                "id": 1,
                "vehicle_plate": "ABC-1234",
                "inspection_date": "2024-12-25",
                "status": "scheduled",
                "notes": "Regular inspection",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        ]
    
    POST /api/inspections
        Creates a new inspection record.
        
        Request Body:
        {
            "vehicle_plate": "ABC-1234",
            "inspection_date": "2024-12-25",
            "status": "scheduled",
            "notes": "Regular inspection"
        }
        
        Response: 201 Created
        {
            "id": 1,
            "vehicle_plate": "ABC-1234",
            "inspection_date": "2024-12-25",
            "status": "scheduled",
            "notes": "Regular inspection",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
        
        Error Response: 400 Bad Request
        {
            "inspection_date": ["Inspection date cannot be in the past."]
        }
    """
    
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    
    @swagger_auto_schema(
        operation_description="Retrieve a list of all vehicle inspections",
        responses={
            200: InspectionSerializer(many=True),
            500: "Internal Server Error"
        },
        tags=['Inspections']
    )
    def get(self, request, *args, **kwargs):
        """Handle GET requests to list all inspections."""
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="""
        Create a new vehicle inspection.
        
        Business Rules:
        - inspection_date cannot be in the past
        - status must be one of: "scheduled", "passed", "failed"
        - vehicle_plate is required
        """,
        request_body=InspectionSerializer,
        responses={
            201: InspectionSerializer(),
            400: "Bad Request - Validation Error"
        },
        tags=['Inspections']
    )
    def post(self, request, *args, **kwargs):
        """Handle POST requests to create a new inspection."""
        return super().post(request, *args, **kwargs)


class InspectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, or deleting a specific inspection.
    
    GET /api/inspections/{id}
        Retrieves a single inspection by ID.
        
        Response: 200 OK
        {
            "id": 1,
            "vehicle_plate": "ABC-1234",
            "inspection_date": "2024-12-25",
            "status": "scheduled",
            "notes": "Regular inspection",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
        
        Error Response: 404 Not Found
        {
            "detail": "Not found."
        }
    
    PUT /api/inspections/{id}
        Updates an existing inspection (full update).
        
        Request Body:
        {
            "vehicle_plate": "ABC-1234",
            "inspection_date": "2024-12-26",
            "status": "passed",
            "notes": "Inspection completed successfully"
        }
        
        Response: 200 OK
        {
            "id": 1,
            "vehicle_plate": "ABC-1234",
            "inspection_date": "2024-12-26",
            "status": "passed",
            "notes": "Inspection completed successfully",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-16T14:20:00Z"
        }
    
    PATCH /api/inspections/{id}
        Partially updates an existing inspection.
        
        Request Body:
        {
            "status": "failed",
            "notes": "Failed brake inspection"
        }
        
        Response: 200 OK
    
    DELETE /api/inspections/{id}
        Deletes an inspection.
        
        Response: 204 No Content
    """
    
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    
    @swagger_auto_schema(
        operation_description="Retrieve a specific vehicle inspection by ID",
        responses={
            200: InspectionSerializer(),
            404: "Not Found"
        },
        tags=['Inspections']
    )
    def get(self, request, *args, **kwargs):
        """Handle GET requests to retrieve a specific inspection."""
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="""
        Update an existing vehicle inspection (full update).
        
        All fields must be provided. For partial updates, use PATCH instead.
        """,
        request_body=InspectionSerializer,
        responses={
            200: InspectionSerializer(),
            400: "Bad Request - Validation Error",
            404: "Not Found"
        },
        tags=['Inspections']
    )
    def put(self, request, *args, **kwargs):
        """Handle PUT requests to fully update an inspection."""
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="""
        Partially update an existing vehicle inspection.
        
        Only the provided fields will be updated.
        """,
        request_body=InspectionSerializer,
        responses={
            200: InspectionSerializer(),
            400: "Bad Request - Validation Error",
            404: "Not Found"
        },
        tags=['Inspections']
    )
    def patch(self, request, *args, **kwargs):
        """Handle PATCH requests to partially update an inspection."""
        return super().patch(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Delete a specific vehicle inspection",
        responses={
            204: "No Content - Successfully Deleted",
            404: "Not Found"
        },
        tags=['Inspections']
    )
    def delete(self, request, *args, **kwargs):
        """Handle DELETE requests to remove an inspection."""
        return super().delete(request, *args, **kwargs)
