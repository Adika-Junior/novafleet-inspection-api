# NovaFleet Vehicle Inspection Tracker API

A production-ready RESTful API for managing vehicle inspections, built with Django and Django REST Framework.

## 🚀 Features

- **Complete CRUD Operations**: Create, read, update, and delete vehicle inspections
- **Status-Aware Validation**: Intelligent date validation based on inspection status
  - Future dates required for **scheduled** inspections
  - Past dates allowed for **passed** or **failed** inspections (record historical results)
- **Reschedule Failed Inspections**: Dedicated endpoint to reschedule failed or passed inspections
- **Interactive API Documentation**: Swagger UI and ReDoc for easy API exploration
- **Comprehensive Testing**: 21 automated tests ensuring reliability
- **Audit Trail**: Automatic tracking of inspection status changes with history records
- **Production-Ready Code**: Well-documented, maintainable, and following best practices

## 📋 Project Structure

```
novafleet-inspection-api/
│
├── README.md                    # Main project documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── manage.py                    # Django management script
│
├── config/                      # Django project configuration
│   ├── __init__.py
│   ├── settings.py             # Django settings with CORS
│   ├── urls.py                 # Main URL routing + Swagger
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
│
├── inspections/                 # Main Django application
│   ├── __init__.py
│   ├── admin.py                # Django admin configuration
│   ├── apps.py                 # App configuration
│   ├── models.py               # Inspection data model
│   ├── serializers.py          # DRF serializers with validation
│   ├── views.py                # API views with Swagger docs
│   ├── urls.py                 # App URL routing
│   ├── validators.py           # Custom validation logic
│   ├── tests/                  # Comprehensive test suite
│   │   ├── __init__.py
│   │   ├── test_models.py      # Model validation tests
│   │   └── test_views.py       # API endpoint tests (21 tests including reschedule)
│   └── migrations/             # Database migrations
│       └── __init__.py
│
├── frontend/                    # Web interface
│   ├── index.html              # Basic version with search
│   ├── index-advanced.html     # Advanced version with exports
│   ├── script.js               # Core JavaScript functionality
│   ├── advanced-features.js    # Advanced features (export, stats)
│   ├── styles.css              # Custom CSS styling
│   ├── README.md               # Frontend documentation
│   └── *.md                    # Additional documentation
│
└── db.sqlite3                   # SQLite database (auto-generated)
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd novafleet-inspection-api
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note**: If you see CORS-related errors when using the frontend, make sure `django-cors-headers` is installed:
   ```bash
   pip install django-cors-headers
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - API Base URL: http://localhost:8000/api/
   - Swagger Documentation: http://localhost:8000/swagger/
   - ReDoc Documentation: http://localhost:8000/redoc/
   - Django Admin: http://localhost:8000/admin/

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Endpoints

#### 1. Create a New Inspection
**POST** `/api/inspections`

**Request Body:**
```json
{
  "vehicle_plate": "ABC-1234",
  "inspection_date": "2026-03-15",
  "status": "scheduled",
  "notes": "Regular maintenance inspection"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "vehicle_plate": "ABC-1234",
  "inspection_date": "2026-03-15",
  "status": "scheduled",
  "notes": "Regular maintenance inspection",
  "created_at": "2026-02-05T10:30:00Z",
  "updated_at": "2026-02-05T10:30:00Z"
}
```

#### 2. List All Inspections
**GET** `/api/inspections`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "vehicle_plate": "ABC-1234",
    "inspection_date": "2026-03-15",
    "status": "scheduled",
    "notes": "Regular maintenance inspection",
    "created_at": "2026-02-05T10:30:00Z",
    "updated_at": "2026-02-05T10:30:00Z"
  }
]
```

#### 3. Retrieve a Single Inspection
**GET** `/api/inspections/{id}`

**Response:** `200 OK`
```json
{
  "id": 1,
  "vehicle_plate": "ABC-1234",
  "inspection_date": "2026-03-15",
  "status": "scheduled",
  "notes": "Regular maintenance inspection",
  "created_at": "2026-02-05T10:30:00Z",
  "updated_at": "2026-02-05T10:30:00Z"
}
```

#### 4. Update an Inspection
**PUT** `/api/inspections/{id}`

**Request Body:**
```json
{
  "vehicle_plate": "ABC-1234",
  "inspection_date": "2026-03-15",
  "status": "passed",
  "notes": "Inspection completed successfully"
}
```

**Response:** `200 OK`

#### 5. Partial Update
**PATCH** `/api/inspections/{id}`

**Request Body:**
```json
{
  "status": "failed",
  "notes": "Failed brake inspection"
}
```

**Response:** `200 OK`

#### 6. Delete an Inspection
**DELETE** `/api/inspections/{id}`

**Response:** `204 No Content`

#### 7. Reschedule a Failed/Passed Inspection (NEW!)
**POST** `/api/inspections/{id}/reschedule`

**Purpose**: Reschedule a failed or passed inspection to a new future date with status reset to "scheduled"

**Request Body:**
```json
{
  "new_inspection_date": "2026-03-20",
  "notes": "Rescheduled after brake repair completion"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "vehicle_plate": "ABC-1234",
  "inspection_date": "2026-03-20",
  "status": "scheduled",
  "notes": "Rescheduled after brake repair completion",
  "created_at": "2026-02-05T10:30:00Z",
  "updated_at": "2026-02-05T11:45:00Z"
}
```

**Error Response:** `400 Bad Request`
```json
{
  "error": "Can only reschedule inspections with status 'failed' or 'passed'. Current status: 'scheduled'",
  "current_status": "scheduled",
  "allowed_statuses": ["failed", "passed"]
}
```

### Business Rules & Validation

1. **Intelligent Inspection Date Validation** ⭐ NEW
   - For **"scheduled"** inspections: Date must be in the future
   - For **"passed" or "failed"** inspections: Date can be in the past (to record historical inspections)
   - Error response example:
   ```json
   {
     "inspection_date": ["Inspections scheduled for a past date are not allowed. Today is 2026-02-05, but received 2026-02-04. Note: You can record a historic inspection by using status 'passed' or 'failed'."]
   }
   ```

2. **Status Validation**
   - Status must be one of: `"scheduled"`, `"passed"`, or `"failed"`
   - Error response example:
   ```json
   {
     "status": ["Invalid status \"invalid\". Status must be one of: scheduled, passed, failed."]
   }
   ```

3. **Required Fields**
   - `vehicle_plate`: Required
   - `inspection_date`: Required
   - `status`: Required (defaults to "scheduled")
   - `notes`: Optional

4. **Reschedule Rules** ⭐ NEW
   - Only inspections with status "failed" or "passed" can be rescheduled
   - Rescheduled inspections reset to "scheduled" status
   - New inspection date must be in the future
   - Previous status change is tracked in inspection history

## 🧪 Running Tests

The project includes comprehensive automated tests covering all requirements and new features.

### Run all tests
```bash
python manage.py test
```

### Run specific test modules
```bash
# Test API endpoints (including reschedule tests)
python manage.py test inspections.tests.test_views

# Test models
python manage.py test inspections.tests.test_models
```

### Run the two required tests
```bash
# Test 1: Successful inspection creation
python manage.py test inspections.tests.test_views.InspectionAPITest.test_create_inspection_with_valid_data

# Test 2: Reject scheduled inspections with past dates
python manage.py test inspections.tests.test_views.InspectionAPITest.test_reject_inspection_with_past_date
```

### Run reschedule tests (NEW!)
```bash
# Test successful reschedule of failed inspection
python manage.py test inspections.tests.test_views.InspectionRescheduleTest.test_reschedule_failed_inspection

# Test reschedule cannot be scheduled past date
python manage.py test inspections.tests.test_views.InspectionRescheduleTest.test_reschedule_with_past_date_rejected
```

### Expected Test Output
```
Found 21 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................
----------------------------------------------------------------------
Ran 21 tests in 0.XXXs

OK
Destroying test database for alias 'default'...
```

## 🧪 Interactive API Testing

### Using Swagger UI
1. Navigate to http://localhost:8000/swagger/
2. Explore all available endpoints
3. Click "Try it out" on any endpoint
4. Fill in the request parameters
5. Click "Execute" to test the API

### Using the Frontend Interface
1. **Start the frontend server** (in a new terminal):
   ```bash
   cd frontend
   python -m http.server 3000
   ```
   **Note**: Make sure to type `http.server` correctly (not `http.sever`)

2. **Access the frontend**: http://localhost:3000
3. **Test all features**:
   - View dashboard statistics
   - Create new inspections
   - Edit existing inspections
   - Delete inspections
   - Test form validation

### Frontend Setup Notes
- **No virtual environment needed** for the frontend - it's pure HTML/CSS/JavaScript (no Python required)
- **No dependencies to install** - Frontend runs standalone with just Python's built-in http.server
- **CORS is configured** in Django to allow frontend connections
- **Both servers must be running**: Django (port 8000) + Frontend (port 3000)

**To run frontend without activating venv**:
```bash
# From the frontend directory (in a NEW terminal, no venv needed)
cd frontend
python -m http.server 3000
# Frontend will be available at http://localhost:3000
```

The frontend is completely independent - it communicates with the Django API via HTTP requests, no shared Python environment needed.

### Using cURL

**Create an inspection:**
```bash
curl -X POST http://localhost:8000/api/inspections \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_plate": "ABC-1234",
    "inspection_date": "2026-03-15",
    "status": "scheduled",
    "notes": "Regular inspection"
  }'
```

**List all inspections:**
```bash
curl http://localhost:8000/api/inspections
```

**Get a specific inspection:**
```bash
curl http://localhost:8000/api/inspections/1
```

**Update an inspection:**
```bash
curl -X PUT http://localhost:8000/api/inspections/1 \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_plate": "ABC-1234",
    "inspection_date": "2026-03-15",
    "status": "passed",
    "notes": "Inspection completed"
  }'
```

## 🎯 Frontend Web Interface

A modern, responsive web interface is included for easy interaction with the API.

### Two Versions Available

#### **Basic Version** (`frontend/index.html`)
- Dashboard with real-time statistics
- Add/edit/delete inspections
- **Simple search by vehicle plate**
- Responsive design
- Form validation

#### **Advanced Version** (`frontend/index-advanced.html`)
- All basic features PLUS:
- Data export (CSV/JSON)
- Advanced statistics modal
- Offline support with auto-sync
- Enhanced UI components

### Quick Frontend Setup
```bash
# 1. Ensure backend is running
python manage.py runserver

# 2. In a new terminal, start frontend (NO virtual environment needed)
cd frontend
python -m http.server 3000
```

### Access URLs
- **Basic Interface**: http://localhost:3000/index.html
- **Advanced Interface**: http://localhost:3000/index-advanced.html
- **Backend API**: http://localhost:8000/api/inspections
- **API Documentation**: http://localhost:8000/swagger/

### Search Functionality
Both versions include **vehicle plate search**:
- **Real-time filtering**: Results update as you type
- **Partial matching**: "ABC" finds "ABC-1234", "DEF-ABC", etc.
- **Case insensitive**: Works with any case
- **Clear search**: One-click to show all inspections

### Technology Stack
- **Django 4.2.9**: Robust web framework with excellent ORM and admin interface
- **Django REST Framework 3.14.0**: Powerful toolkit for building Web APIs
- **drf-yasg 1.21.7**: Automatic Swagger/OpenAPI documentation generation
- **SQLite**: Lightweight database perfect for development and testing

### Code Organization
- **Separation of Concerns**: Models, serializers, views, and validators are in separate modules
- **DRY Principle**: Reusable validators and base configurations
- **RESTful Design**: Standard HTTP methods and status codes
- **Comprehensive Documentation**: Docstrings on all classes and methods

### Validation Strategy
- **Model-level validation**: Ensures data integrity at the database level
- **Serializer-level validation**: Provides detailed API error messages
- **Custom validators**: Reusable validation logic for business rules

### Testing Approach
- **Unit tests**: Test individual components (models, validators)
- **Integration tests**: Test API endpoints end-to-end
- **Edge cases**: Test validation rules and error handling

## � Challenges Experienced During Development

### 1. Date Validation Consistency

**Challenge**: Ensuring date validation works consistently across API and database while supporting real-world workflows.

**Problem Encountered**: 
- Initial implementation rejected ALL past dates
- Users needed to record historical inspections (inspection happened Feb 1, recorded Feb 5)
- Simple regex/date check was too restrictive

**Solution**:
- Implemented status-aware validation
- Only "scheduled" inspections require future dates
- "passed" and "failed" inspections can have any date
- Validation at both serializer (API feedback) and model (data integrity) levels

### 2. Simultaneous Server Management

**Challenge**: Front-end requires Python/Django backend running, but is also pure HTML/CSS/JS.

**Problem Encountered**:
- Users confused about needing venv for frontend
- Frontend needs backend API, but not Python dependencies
- Two server processes must run simultaneously

**Solution**:
- Clarified frontend needs only Python built-in http.server (no venv)
- Provided clear instructions for running both servers
- CORS configuration allows frontend-to-backend communication
- Added separate terminal instructions

### 3. Test Data with Dynamic Dates

**Challenge**: Writing tests that remain valid regardless of when executed.

**Problem Encountered**:
- Hardcoded dates become invalid over time
- Tests that pass today fail next month
- Need to test both valid future dates and invalid past dates

**Solution**:
- Used `timedelta` for relative dates
- `date.today() + timedelta(days=7)` always future, always valid
- Tests never expire, work in any timezone

### 4. URL Pattern Design for Reschedule

**Challenge**: How to express "reschedule" operation in REST API?

**Problem Encountered**:
- Could use PATCH to update inspection_date
- But lose semantic clarity (is this reschedule or edit?)
- Users confused about workflow

**Solution**:
- Created dedicated `POST /api/inspections/{id}/reschedule` endpoint
- Clear intent: this is a reschedule operation
- Automatic status reset to "scheduled"
- Validates only failed/passed inspections can reschedule
- History automatically tracks the reschedule event

### 5. Error Message Quality

**Challenge**: Providing helpful error messages without exposing internals.

**Problem Encountered**:
- Generic errors don't help users fix their requests
- Need to explain what's wrong AND how to fix it
- Can't expose security-sensitive information

**Solution**:
- Detailed error messages with context
- Include what was wrong + what was expected
- Example: "Scheduled inspections must have future dates. Today is 2026-02-05, but received 2026-02-04. Use status 'passed' or 'failed' to record historical inspections."
- Consistent error response format across API

### 6. CORS Configuration

**Challenge**: Frontend on port 3000 connecting to API on port 8000.

**Problem Encountered**:
- Browser blocks cross-origin requests by default
- Without CORS, frontend can't communicate with API
- Django doesn't include CORS by default

**Solution**:
- Installed django-cors-headers
- Configured CORS_ALLOWED_ORIGINS in settings
- Allows frontend safe access to API
- Documented in requirements.txt

### 7. API Documentation Maintenance

**Challenge**: Keeping API docs in sync with code.

**Problem Encountered**:
- Manual documentation gets outdated
- Changes to code aren't reflected in docs
- Developers forget to update documentation

**Solution**:
- Used drf-yasg for auto-generated Swagger docs
- Added @swagger_auto_schema decorators
- Documentation generated from code
- Always accurate, never outdated

## �🔧 Troubleshooting

### Common Setup Issues

**1. CORS Errors in Frontend**
```bash
# Install CORS support
pip install django-cors-headers
# Restart Django server
python manage.py runserver
```

**2. "No module named 'corsheaders'"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
pip install django-cors-headers
```

**3. "No module named http.sever"**
```bash
# Fix typo: use http.server (not http.sever)
python -m http.server 3000
```

**4. Frontend Can't Connect to API**
- Ensure Django server is running on port 8000
- Ensure frontend server is running on port 3000
- Frontend doesn't need venv - just run `python -m http.server 3000` from frontend directory

**5. "Frontend needs to be in venv"**
- **No it doesn't!** Frontend is pure HTML/CSS/JavaScript
- You only need Django in venv (for the API)
- Frontend can run in ANY Python environment with `python -m http.server 3000`
- No dependencies to install for frontend
- Check browser console (F12) for error messages

**5. Tests Failing**
```bash
# Stop the development server first
# Then run tests
python manage.py test
```

## 💡 Development Tips

- **Backend**: Requires virtual environment and dependencies
- **Frontend**: No virtual environment needed (pure HTML/CSS/JS)
- **Two Terminals**: Run backend and frontend servers simultaneously
- **CORS**: Already configured for localhost:3000 ↔ localhost:8000

1. **Date Validation Timing**
   - Challenge: Ensuring consistent date validation across model and serializer layers
   - Solution: Implemented validation at both levels with clear error messages

2. **Swagger Documentation**
   - Challenge: Generating comprehensive API documentation automatically
   - Solution: Used drf-yasg with custom schema annotations for detailed endpoint descriptions

3. **Test Data Management**
   - Challenge: Creating reliable tests that work regardless of when they're run
   - Solution: Used relative dates (date.today() + timedelta) instead of hardcoded dates

## 🚀 Future Enhancements

Given additional time, I would implement:

1. **Authentication & Authorization**
   - JWT token-based authentication
   - Role-based access control (admin, inspector, viewer)
   - User-specific inspection history

2. **Advanced Filtering & Search**
   - Filter inspections by date range, status, or vehicle
   - Full-text search on notes
   - Pagination for large datasets

3. **File Attachments**
   - Upload inspection photos
   - Attach PDF reports
   - Store documents in cloud storage (AWS S3)

4. **Notifications**
   - Email reminders for upcoming inspections
   - SMS alerts for failed inspections
   - Webhook integrations for third-party systems

5. **Analytics & Reporting**
   - Dashboard with inspection statistics
   - Export data to CSV/Excel
   - Generate PDF inspection reports

6. **Enhanced Validation**
   - Vehicle plate format validation by region
   - Duplicate inspection detection
   - Inspection scheduling conflicts

7. **Production Deployment**
   - PostgreSQL database
   - Docker containerization
   - CI/CD pipeline with GitHub Actions
   - Environment-based configuration
   - Logging and monitoring (Sentry, DataDog)

8. **API Versioning**
   - Version the API (v1, v2) for backward compatibility
   - Deprecation warnings for old endpoints

9. **Rate Limiting**
   - Prevent API abuse
   - Throttling for different user tiers

10. **Internationalization**
    - Multi-language support
    - Localized date formats
    - Currency and unit conversions

## 📝 Development Notes

- The project uses SQLite for simplicity in development
- All code follows PEP 8 style guidelines
- Comprehensive inline comments explain complex logic
- The API returns consistent JSON responses
- Error messages are user-friendly and actionable

## 🤝 Contributing

Feedback is welcome! If you notice any issues or have suggestions:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - Feel free to use for personal and commercial projects.
