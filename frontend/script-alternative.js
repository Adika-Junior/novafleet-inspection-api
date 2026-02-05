// Alternative implementation with individual API calls for each inspection

// Edit inspection with individual API call
async function editInspectionWithApiCall(id) {
    try {
        // GET /api/inspections/{id} - Individual API call
        const response = await fetch(`${API_BASE_URL}/inspections/${id}`);
        
        if (response.ok) {
            const inspection = await response.json();
            
            // Populate edit form
            document.getElementById('editId').value = inspection.id;
            document.getElementById('editVehiclePlate').value = inspection.vehicle_plate;
            document.getElementById('editInspectionDate').value = inspection.inspection_date;
            document.getElementById('editStatus').value = inspection.status;
            document.getElementById('editNotes').value = inspection.notes || '';
            
            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('editModal'));
            modal.show();
        } else {
            showAlert('Failed to load inspection details.', 'danger');
        }
    } catch (error) {
        console.error('Error fetching inspection:', error);
        showAlert('Failed to load inspection. Please check your connection.', 'danger');
    }
}

// View single inspection details (if you want a detail view)
async function viewInspectionDetails(id) {
    try {
        // GET /api/inspections/{id}
        const response = await fetch(`${API_BASE_URL}/inspections/${id}`);
        
        if (response.ok) {
            const inspection = await response.json();
            
            // Display inspection details in a modal or separate view
            showInspectionDetailsModal(inspection);
        } else {
            showAlert('Failed to load inspection details.', 'danger');
        }
    } catch (error) {
        console.error('Error fetching inspection:', error);
        showAlert('Failed to load inspection. Please check your connection.', 'danger');
    }
}

function showInspectionDetailsModal(inspection) {
    // Create and show a details modal
    const detailsHtml = `
        <div class="modal fade" id="detailsModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Inspection Details</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p><strong>ID:</strong> ${inspection.id}</p>
                        <p><strong>Vehicle Plate:</strong> ${inspection.vehicle_plate}</p>
                        <p><strong>Inspection Date:</strong> ${formatDate(inspection.inspection_date)}</p>
                        <p><strong>Status:</strong> ${inspection.status}</p>
                        <p><strong>Notes:</strong> ${inspection.notes || 'No notes'}</p>
                        <p><strong>Created:</strong> ${formatDateTime(inspection.created_at)}</p>
                        <p><strong>Updated:</strong> ${formatDateTime(inspection.updated_at)}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" onclick="editInspection(${inspection.id})">Edit</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to page and show it
    document.body.insertAdjacentHTML('beforeend', detailsHtml);
    const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
    modal.show();
    
    // Remove modal from DOM when hidden
    document.getElementById('detailsModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}