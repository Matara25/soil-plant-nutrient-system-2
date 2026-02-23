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
        const farmerList = document.getElementById('farmerList');
        if (!farmerList) return;

        farmerList.innerHTML = '';

        farmers.forEach(farmer => {
            const farmerItem = document.createElement('div');
            farmerItem.className = 'farmer-item';
            farmerItem.innerHTML = `
                <div class="farmer-info">
                    <div class="farmer-name">${farmer.name}</div>
                    <div class="farmer-details">
                        <div>📧 ${farmer.email}</div>
                        <div>📱 ${farmer.phone}</div>
                        <div>📍 ${farmer.location || 'Not specified'}</div>
                        <div>📅 Joined: ${farmer.joinedDate}</div>
                        <div>🏷️ Status: <span style="color: ${farmer.status === 'active' ? 'var(--accent-green)' : 'var(--danger-red)'}">${farmer.status}</span></div>
                    </div>
                </div>
                <div class="farmer-actions">
                    <button class="btn-assign" onclick="farmerManager.showCropAssignment(${farmer.id})">
                        <i class="fas fa-seedling"></i> Assign Crops
                    </button>
                    <button class="btn-delete" onclick="farmerManager.deleteFarmer(${farmer.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
            farmerList.appendChild(farmerItem);
        });

        // Update statistics
        this.updateStatistics();
    }

    addFarmer() {
        const name = document.getElementById('farmerName').value.trim();
        const email = document.getElementById('farmerEmail').value.trim();
        const phone = document.getElementById('farmerPhone').value.trim();
        const location = document.getElementById('farmerLocation').value.trim();

        if (!name || !email || !phone || !location) {
            alert('Please fill in all fields');
            return;
        }

        const newFarmer = window.farmDB.addFarmer({
            name,
            email,
            phone,
            location
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
        document.getElementById('cropAssignmentModal').style.display = 'block';
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
        document.getElementById('addFarmerModal').style.display = 'block';
        document.getElementById('addFarmerForm').reset();
    }

    closeAddFarmerModal() {
        console.log('Close add farmer modal called');
        document.getElementById('addFarmerModal').style.display = 'none';
    }

    closeCropAssignmentModal() {
        console.log('Close crop assignment modal called');
        document.getElementById('cropAssignmentModal').style.display = 'none';
        this.currentFarmerId = null;
    }

    closeAllModals() {
        this.closeAddFarmerModal();
        this.closeCropAssignmentModal();
    }
}

// Initialize farmer management when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing farmer management...');
    window.farmerManager = new FarmerManagement();
    
    // Make sure global functions are available
    window.showAddFarmerModal = function() {
        console.log('Show add farmer modal called');
        if (window.farmerManager) {
            window.farmerManager.showAddFarmerModal();
        } else {
            console.error('Farmer manager not initialized');
        }
    };
    
    window.closeAddFarmerModal = function() {
        console.log('Close add farmer modal called');
        if (window.farmerManager) {
            window.farmerManager.closeAddFarmerModal();
        }
    };
    
    window.closeCropAssignmentModal = function() {
        console.log('Close crop assignment modal called');
        if (window.farmerManager) {
            window.farmerManager.closeCropAssignmentModal();
        }
    };
    
    console.log('Farmer management initialized successfully');
});
