// Farmer Management System
class FarmerManagement {
    constructor() {
        this.currentFarmerId = null;
        this.init();
    }

    init() {
        this.loadFarmers();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Add farmer form
        const addFarmerForm = document.getElementById('addFarmerForm');
        if (addFarmerForm) {
            addFarmerForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.addFarmer();
            });
        }

        // Crop assignment form
        const cropAssignmentForm = document.getElementById('cropAssignmentForm');
        if (cropAssignmentForm) {
            cropAssignmentForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.assignCrops();
            });
        }

        // Close modals when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeAllModals();
            }
        });
    }

    loadFarmers() {
        const farmers = window.farmDB.getAllFarmers();
        this.displayFarmers(farmers);
    }

    displayFarmers(farmers) {
        console.log('Displaying farmers:', farmers);
        const tableBody = document.getElementById('farmerTableBody');
        const noFarmersMessage = document.getElementById('noFarmersMessage');
        const farmerTable = document.getElementById('farmerTable');
        
        console.log('Elements found:', {
            tableBody: !!tableBody,
            noFarmersMessage: !!noFarmersMessage,
            farmerTable: !!farmerTable
        });
        
        if (!tableBody) {
            console.error('Table body not found!');
            return;
        }

        tableBody.innerHTML = '';

        if (farmers.length === 0) {
            if (farmerTable) farmerTable.style.display = 'none';
            if (noFarmersMessage) noFarmersMessage.style.display = 'block';
            console.log('No farmers to display');
            return;
        }

        if (farmerTable) farmerTable.style.display = 'table';
        if (noFarmersMessage) noFarmersMessage.style.display = 'none';

        farmers.forEach(farmer => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <i class="fas fa-user-circle" style="color: var(--accent-green);"></i>
                        ${farmer.name}
                    </div>
                </td>
                <td>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <i class="fas fa-envelope" style="color: var(--medium-gray); font-size: 0.8rem;"></i>
                        ${farmer.email}
                    </div>
                </td>
                <td>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <i class="fas fa-phone" style="color: var(--medium-gray); font-size: 0.8rem;"></i>
                        ${farmer.phone}
                    </div>
                </td>
                <td>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <i class="fas fa-map-marker-alt" style="color: var(--medium-gray); font-size: 0.8rem;"></i>
                        ${farmer.location || 'Not specified'}
                    </div>
                </td>
                <td>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <i class="fas fa-ruler-combined" style="color: var(--accent-green); font-size: 0.8rem;"></i>
                        ${farmer.farmSize || 'Not specified'}
                    </div>
                </td>
                <td>
                    <span class="status-badge active">
                        <i class="fas fa-clock" style="margin-right: 4px;"></i>
                        ${farmer.experience || 'Not specified'}
                    </span>
                </td>
                <td>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <i class="fas fa-calendar" style="color: var(--medium-gray); font-size: 0.8rem;"></i>
                        ${farmer.joinedDate}
                    </div>
                </td>
                <td>
                    <div class="table-actions">
                        <button class="btn-table btn-assign-crops" onclick="showCropAssignment(${farmer.id})">
                            <i class="fas fa-seedling"></i> Assign Crops
                        </button>
                        <button class="btn-table btn-delete-farmer" onclick="deleteFarmer(${farmer.id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </td>
            `;
            tableBody.appendChild(row);
        });

        console.log('Table populated successfully');
        // Update statistics
        this.updateStatistics();
    }

    addFarmer() {
        const name = document.getElementById('farmerName').value.trim();
        const email = document.getElementById('farmerEmail').value.trim();
        const phone = document.getElementById('farmerPhone').value.trim();
        const location = document.getElementById('farmerLocation').value.trim();
        const farmSize = document.getElementById('farmSize').value.trim();
        const experience = document.getElementById('experience').value;

        if (!name || !email || !phone || !location) {
            alert('Please fill in all required fields');
            return;
        }

        const newFarmer = window.farmDB.addFarmer({
            name,
            email,
            phone,
            location,
            farmSize: farmSize || 'Not specified',
            experience: experience || 'Not specified'
        });

        alert(`Farmer "${newFarmer.name}" has been added successfully!`);
        this.closeAddFarmerModal();
        this.loadFarmers();
    }

    deleteFarmer(farmerId) {
        if (confirm('Are you sure you want to delete this farmer? This will also remove all their crop assignments.')) {
            const success = window.farmDB.deleteFarmer(farmerId);
            if (success) {
                alert('Farmer deleted successfully');
                this.loadFarmers();
            } else {
                alert('Error deleting farmer');
            }
        }
    }

    showCropAssignment(farmerId) {
        this.currentFarmerId = farmerId;
        const farmer = window.farmDB.getFarmer(farmerId);
        const crops = window.farmDB.getAllCrops();
        const farmerCrops = window.farmDB.getFarmerCrops(farmerId);

        // Display farmer info
        const farmerInfo = document.getElementById('selectedFarmerInfo');
        farmerInfo.innerHTML = `
            <div class="farmer-info-display">
                <h4>${farmer.name}</h4>
                <p>📧 ${farmer.email}</p>
                <p>📱 ${farmer.phone}</p>
                <p>📍 ${farmer.location || 'Not specified'}</p>
            </div>
        `;

        // Display crop checkboxes
        const cropCheckboxes = document.getElementById('cropCheckboxes');
        cropCheckboxes.innerHTML = '';

        crops.forEach(crop => {
            const isAssigned = farmerCrops.some(fc => fc.cropId === crop.id);
            const checkboxDiv = document.createElement('div');
            checkboxDiv.className = 'crop-checkbox';
            checkboxDiv.innerHTML = `
                <input type="checkbox" id="crop_${crop.id}" value="${crop.id}" ${isAssigned ? 'checked' : ''}>
                <label for="crop_${crop.id}">
                    <strong>${crop.name}</strong> - ${crop.category}
                    <br><small>🌱 ${crop.season} | ⏱️ ${crop.growingDays} days | 💧 ${crop.waterNeeds}</small>
                </label>
            `;
            cropCheckboxes.appendChild(checkboxDiv);
        });

        // Show modal
        const modal = document.getElementById('cropAssignmentModal');
        if (modal) {
            modal.style.display = 'block';
            modal.style.zIndex = '100000';
        }
    }

    assignCrops() {
        if (!this.currentFarmerId) return;

        const checkedBoxes = document.querySelectorAll('#cropCheckboxes input[type="checkbox"]:checked');
        const plantingDate = document.getElementById('plantingDate').value;
        const expectedHarvest = document.getElementById('expectedHarvest').value;

        if (checkedBoxes.length === 0) {
            alert('Please select at least one crop');
            return;
        }

        if (!plantingDate || !expectedHarvest) {
            alert('Please select planting and expected harvest dates');
            return;
        }

        // Remove existing crop assignments for this farmer
        const existingAssignments = window.farmDB.getFarmerCrops(this.currentFarmerId);
        existingAssignments.forEach(assignment => {
            window.farmDB.removeCropFromFarmer(this.currentFarmerId, assignment.cropId);
        });

        // Add new crop assignments
        checkedBoxes.forEach(checkbox => {
            const cropId = parseInt(checkbox.value);
            window.farmDB.assignCropToFarmer(this.currentFarmerId, cropId, {
                plantedDate,
                expectedHarvest,
                status: 'growing'
            });
        });

        alert('Crops assigned successfully!');
        this.closeCropAssignmentModal();
        this.loadFarmers();
    }

    updateStatistics() {
        const stats = window.farmDB.getStatistics();
        
        // Update farm overview stats if they exist
        const totalAreaElement = document.querySelector('.farm-stats .stat-value');
        const activeCropsElement = document.querySelectorAll('.farm-stats .stat-value')[1];
        const soilHealthElement = document.querySelectorAll('.farm-stats .stat-value')[2];

        if (totalAreaElement) totalAreaElement.textContent = `${stats.totalFarmers} Farmers`;
        if (activeCropsElement) activeCropsElement.textContent = `${stats.totalAssignments} Crops`;
        if (soilHealthElement) soilHealthElement.textContent = `${stats.totalCrops} Types`;
    }

    // Modal management
    showAddFarmerModal() {
        console.log('Show add farmer modal called');
        const modal = document.getElementById('addFarmerModal');
        console.log('Modal element found:', !!modal);
        
        if (modal) {
            // Force show modal with maximum priority
            modal.style.display = 'block';
            modal.style.visibility = 'visible';
            modal.style.opacity = '1';
            modal.style.zIndex = '999999';
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
            
            // Also ensure modal content is visible
            const modalContent = modal.querySelector('.modal-content');
            if (modalContent) {
                modalContent.style.display = 'block';
                modalContent.style.visibility = 'visible';
                modalContent.style.opacity = '1';
                modalContent.style.zIndex = '1000000';
            }
            
            const form = document.getElementById('addFarmerForm');
            if (form) {
                form.reset();
            }
            
            console.log('Modal styles applied:', modal.style.cssText);
        } else {
            console.error('Add farmer modal not found in DOM');
        }
    }

    closeAddFarmerModal() {
        const modal = document.getElementById('addFarmerModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    closeCropAssignmentModal() {
        const modal = document.getElementById('cropAssignmentModal');
        if (modal) {
            modal.style.display = 'none';
        }
        this.currentFarmerId = null;
    }

    closeAllModals() {
        this.closeAddFarmerModal();
        this.closeCropAssignmentModal();
    }
}

// Global functions for onclick handlers
function showAddFarmerModal() {
    console.log('Show add farmer modal called');
    if (window.farmerManager) {
        window.farmerManager.showAddFarmerModal();
    } else {
        console.error('Farmer manager not initialized');
    }
}

function closeAddFarmerModal() {
    console.log('Close add farmer modal called');
    if (window.farmerManager) {
        window.farmerManager.closeAddFarmerModal();
    }
}

function closeCropAssignmentModal() {
    console.log('Close crop assignment modal called');
    if (window.farmerManager) {
        window.farmerManager.closeCropAssignmentModal();
    }
}

function showCropAssignment(farmerId) {
    console.log('Show crop assignment called for farmer:', farmerId);
    if (window.farmerManager) {
        window.farmerManager.showCropAssignment(farmerId);
    }
}

function deleteFarmer(farmerId) {
    console.log('Delete farmer called for:', farmerId);
    if (window.farmerManager) {
        window.farmerManager.deleteFarmer(farmerId);
    }
}

// Initialize farmer management when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing farmer management...');
    window.farmerManager = new FarmerManagement();
    console.log('Farmer management initialized successfully');
    
    // Test function
    window.testModal = function() {
        console.log('Test modal called');
        alert('Test function working! Now try Add Farmer button.');
    };
});
