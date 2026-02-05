// NovaFleet Inspection Tracker - JavaScript

const API_BASE_URL = 'http://localhost:8000/api';
let inspections = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('inspectionDate').min = today;
    document.getElementById('editInspectionDate').min = today;
    
    // Load initial data
    loadInspections();
    
    // Set up form submission
    document.getElementById('inspectionForm').addEventListener('submit', handleFormSubmit);
});

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = {
        vehicle_plate: document.getElementById('vehiclePlate').value.trim().toUpperCase(),
        inspection_date: document.getElementById('inspectionDate').value,
        status: document.getElementById('status').value,
        notes: document.getElementById('notes').value.trim() || null
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/inspections`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            const newInspection = await response.json();
            showAlert('Inspection scheduled successfully!', 'success');
            document.getElementById('inspectionForm').reset();
            loadInspections(); // Refresh the list
        } else {
            const errorData = await response.json();
            handleApiError(errorData);
        }
    } catch (error) {
        console.error('Error creating inspection:', error);
        showAlert('Failed to create inspection. Please check your connection.', 'danger');
    }
}

// Load all inspections
async function loadInspections() {
    try {
        const response = await fetch(`${API_BASE_URL}/inspections`);
        
        if (response.ok) {
            const data = await response.json();
            inspections = data.results || data; // Handle both paginated and non-paginated responses
            renderInspections();
            updateStatistics();
        } else {
            throw new Error('Failed to load inspections');
        }
    } catch (error) {
        console.error('Error loading inspections:', error);
        showAlert('Failed to load inspections. Please check your connection.', 'danger');
        renderEmptyState();
    }
}

// Render inspections table
function renderInspections() {
    const tbody = document.getElementById('inspectionsTableBody');
    
    if (inspections.length === 0) {
        renderEmptyState();
        return;
    }
    
    tbody.innerHTML = inspections.map(inspection => `
        <tr class="fade-in">
            <td><strong>#${inspection.id}</strong></td>
            <td>
                <i class="fas fa-truck text-primary me-1"></i>
                <strong>${inspection.vehicle_plate}</strong>
            </td>
            <td>${formatDate(inspection.inspection_date)}</td>
            <td>${renderStatusBadge(inspection.status)}</td>
            <td class="notes-cell" title="${inspection.notes || ''}">${inspection.notes || '<em class="text-muted">No notes</em>'}</td>
            <td class="text-muted">${formatDateTime(inspection.created_at)}</td>
            <td>
                <button class="btn btn-outline-primary btn-action" onclick="editInspection(${inspection.id})" title="Edit">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-outline-danger btn-action" onclick="deleteInspection(${inspection.id})" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// Render empty state
function renderEmptyState() {
    const tbody = document.getElementById('inspectionsTableBody');
    tbody.innerHTML = `
        <tr>
            <td colspan="7" class="empty-state">
                <i class="fas fa-clipboard-list"></i>
                <h5>No inspections found</h5>
                <p class="text-muted">Schedule your first inspection using the form above.</p>
            </td>
        </tr>
    `;
}

// Render status badge
function renderStatusBadge(status) {
    const statusConfig = {
        scheduled: { class: 'badge-scheduled', icon: 'clock', text: 'Scheduled' },
        passed: { class: 'badge-passed', icon: 'check-circle', text: 'Passed' },
        failed: { class: 'badge-failed', icon: 'times-circle', text: 'Failed' }
    };
    
    const config = statusConfig[status] || { class: 'bg-secondary', icon: 'question', text: status };
    
    return `
        <span class="badge ${config.class}">
            <i class="fas fa-${config.icon} status-icon"></i>${config.text}
        </span>
    `;
}

// Update statistics
function updateStatistics() {
    const total = inspections.length;
    const scheduled = inspections.filter(i => i.status === 'scheduled').length;
    const passed = inspections.filter(i => i.status === 'passed').length;
    const failed = inspections.filter(i => i.status === 'failed').length;
    
    document.getElementById('totalInspections').textContent = total;
    document.getElementById('scheduledInspections').textContent = scheduled;
    document.getElementById('passedInspections').textContent = passed;
    document.getElementById('failedInspections').textContent = failed;
}

// Edit inspection
function editInspection(id) {
    const inspection = inspections.find(i => i.id === id);
    if (!inspection) return;
    
    // Populate edit form
    document.getElementById('editId').value = inspection.id;
    document.getElementById('editVehiclePlate').value = inspection.vehicle_plate;
    document.getElementById('editInspectionDate').value = inspection.inspection_date;
    document.getElementById('editStatus').value = inspection.status;
    document.getElementById('editNotes').value = inspection.notes || '';
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('editModal'));
    modal.show();
}

// Update inspection
async function updateInspection() {
    const id = document.getElementById('editId').value;
    const formData = {
        vehicle_plate: document.getElementById('editVehiclePlate').value.trim().toUpperCase(),
        inspection_date: document.getElementById('editInspectionDate').value,
        status: document.getElementById('editStatus').value,
        notes: document.getElementById('editNotes').value.trim() || null
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/inspections/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showAlert('Inspection updated successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('editModal')).hide();
            loadInspections(); // Refresh the list
        } else {
            const errorData = await response.json();
            handleApiError(errorData);
        }
    } catch (error) {
        console.error('Error updating inspection:', error);
        showAlert('Failed to update inspection. Please check your connection.', 'danger');
    }
}

// Delete inspection
async function deleteInspection(id) {
    const inspection = inspections.find(i => i.id === id);
    if (!inspection) return;
    
    if (!confirm(`Are you sure you want to delete the inspection for ${inspection.vehicle_plate}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/inspections/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showAlert('Inspection deleted successfully!', 'success');
            loadInspections(); // Refresh the list
        } else {
            throw new Error('Failed to delete inspection');
        }
    } catch (error) {
        console.error('Error deleting inspection:', error);
        showAlert('Failed to delete inspection. Please check your connection.', 'danger');
    }
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    const alertId = 'alert-' + Date.now();
    
    const alertHtml = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="fas fa-${getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.insertAdjacentHTML('beforeend', alertHtml);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alertElement = document.getElementById(alertId);
        if (alertElement) {
            const alert = bootstrap.Alert.getOrCreateInstance(alertElement);
            alert.close();
        }
    }, 5000);
}

// Get alert icon based on type
function getAlertIcon(type) {
    const icons = {
        success: 'check-circle',
        danger: 'exclamation-triangle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Handle API errors
function handleApiError(errorData) {
    let message = 'An error occurred. Please try again.';
    
    if (typeof errorData === 'object') {
        const errors = [];
        for (const [field, messages] of Object.entries(errorData)) {
            if (Array.isArray(messages)) {
                errors.push(`${field}: ${messages.join(', ')}`);
            } else {
                errors.push(`${field}: ${messages}`);
            }
        }
        if (errors.length > 0) {
            message = errors.join('<br>');
        }
    }
    
    showAlert(message, 'danger');
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format datetime for display
function formatDateTime(dateTimeString) {
    const date = new Date(dateTimeString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Utility function to handle CORS issues in development
function handleCorsError() {
    showAlert(
        'Unable to connect to the API. Make sure the Django server is running on http://localhost:8000 and CORS is properly configured.',
        'danger'
    );
}

// ============================================================================
// SEARCH FUNCTIONALITY
// ============================================================================

let originalInspections = []; // Store original data for search
let searchTimeout; // For debouncing search

// Search inspections by vehicle plate
function searchInspections(searchTerm) {
    // Clear previous timeout
    clearTimeout(searchTimeout);
    
    // Debounce search with 300ms delay
    searchTimeout = setTimeout(() => {
        performSearch(searchTerm.trim());
    }, 300);
}

function performSearch(searchTerm) {
    // Store original data if not already stored
    if (originalInspections.length === 0 && inspections.length > 0) {
        originalInspections = [...inspections];
    }
    
    let filteredInspections;
    
    if (searchTerm === '') {
        // Show all inspections if search is empty
        filteredInspections = originalInspections;
        updateSearchSummary('');
    } else {
        // Filter by vehicle plate (case insensitive)
        filteredInspections = originalInspections.filter(inspection =>
            inspection.vehicle_plate.toLowerCase().includes(searchTerm.toLowerCase())
        );
        updateSearchSummary(searchTerm, filteredInspections.length);
    }
    
    // Update the display
    inspections = filteredInspections;
    renderInspections();
    updateStatistics();
}

function updateSearchSummary(searchTerm, resultCount = null) {
    const summaryElement = document.getElementById('searchSummary');
    if (!summaryElement) return;
    
    if (searchTerm === '') {
        summaryElement.innerHTML = '';
    } else {
        const message = resultCount === 0 ? 
            `No inspections found for "${searchTerm}"` :
            `Found ${resultCount} inspection(s) matching "${searchTerm}"`;
        
        const alertClass = resultCount === 0 ? 'alert-warning' : 'alert-info';
        
        summaryElement.innerHTML = `
            <div class="alert ${alertClass}">
                <i class="fas fa-search me-2"></i>
                ${message}
                <button class="btn btn-sm btn-outline-secondary ms-2" onclick="clearSearch()">
                    <i class="fas fa-times me-1"></i>Clear
                </button>
            </div>
        `;
    }
}

function clearSearch() {
    // Clear search input
    const searchInput = document.getElementById('searchVehiclePlate');
    if (searchInput) {
        searchInput.value = '';
    }
    
    // Reset to original data
    if (originalInspections.length > 0) {
        inspections = [...originalInspections];
        renderInspections();
        updateStatistics();
    }
    
    // Clear search summary
    updateSearchSummary('');
}

// Update loadInspections to store original data
const originalLoadInspections = loadInspections;
loadInspections = async function() {
    await originalLoadInspections();
    // Store original data for search
    originalInspections = [...inspections];
};