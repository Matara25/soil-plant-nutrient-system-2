// Database Management System for Farmers and Crops
class FarmDatabase {
    constructor() {
        this.farmers = [];
        this.crops = [];
        this.farmerCrops = [];
        this.initializeData();
    }

    initializeData() {
        // Load from localStorage or use defaults
        const savedFarmers = localStorage.getItem('farmers');
        const savedCrops = localStorage.getItem('crops');
        const savedFarmerCrops = localStorage.getItem('farmerCrops');

        this.farmers = savedFarmers ? JSON.parse(savedFarmers) : [
            { id: 1, name: 'John Smith', email: 'john@farm.com', phone: '123-456-7890', joinedDate: '2024-01-15', status: 'active' },
            { id: 2, name: 'Mary Johnson', email: 'mary@farm.com', phone: '098-765-4321', joinedDate: '2024-02-20', status: 'active' }
        ];

        this.crops = savedCrops ? JSON.parse(savedCrops) : [
            { id: 1, name: 'Maize', category: 'Grains', season: 'Summer', growingDays: 90, waterNeeds: 'High', soilType: 'Loamy' },
            { id: 2, name: 'Tomatoes', category: 'Vegetables', season: 'Spring', growingDays: 60, waterNeeds: 'Medium', soilType: 'Well-drained' },
            { id: 3, name: 'Wheat', category: 'Grains', season: 'Winter', growingDays: 120, waterNeeds: 'Low', soilType: 'Clay' },
            { id: 4, name: 'Potatoes', category: 'Vegetables', season: 'Spring', growingDays: 80, waterNeeds: 'Medium', soilType: 'Sandy' },
            { id: 5, name: 'Soybeans', category: 'Legumes', season: 'Summer', growingDays: 100, waterNeeds: 'Medium', soilType: 'Loamy' },
            { id: 6, name: 'Carrots', category: 'Vegetables', season: 'Fall', growingDays: 70, waterNeeds: 'Low', soilType: 'Sandy loam' },
            { id: 7, name: 'Rice', category: 'Grains', season: 'Monsoon', growingDays: 110, waterNeeds: 'Very High', soilType: 'Clay loam' },
            { id: 8, name: 'Lettuce', category: 'Vegetables', season: 'Spring', growingDays: 45, waterNeeds: 'Low', soilType: 'Rich loam' }
        ];

        this.farmerCrops = savedFarmerCrops ? JSON.parse(savedFarmerCrops) : [
            { farmerId: 1, cropId: 1, plantedDate: '2024-03-01', expectedHarvest: '2024-05-30', status: 'growing' },
            { farmerId: 1, cropId: 2, plantedDate: '2024-03-15', expectedHarvest: '2024-05-15', status: 'growing' },
            { farmerId: 2, cropId: 3, plantedDate: '2024-02-10', expectedHarvest: '2024-06-10', status: 'growing' }
        ];

        this.saveToLocalStorage();
    }

    saveToLocalStorage() {
        localStorage.setItem('farmers', JSON.stringify(this.farmers));
        localStorage.setItem('crops', JSON.stringify(this.crops));
        localStorage.setItem('farmerCrops', JSON.stringify(this.farmerCrops));
    }

    // Farmer CRUD operations
    addFarmer(farmerData) {
        const newFarmer = {
            id: this.farmers.length > 0 ? Math.max(...this.farmers.map(f => f.id)) + 1 : 1,
            ...farmerData,
            joinedDate: new Date().toISOString().split('T')[0],
            status: 'active'
        };
        this.farmers.push(newFarmer);
        this.saveToLocalStorage();
        return newFarmer;
    }

    updateFarmer(id, farmerData) {
        const index = this.farmers.findIndex(f => f.id === id);
        if (index !== -1) {
            this.farmers[index] = { ...this.farmers[index], ...farmerData };
            this.saveToLocalStorage();
            return this.farmers[index];
        }
        return null;
    }

    deleteFarmer(id) {
        const index = this.farmers.findIndex(f => f.id === id);
        if (index !== -1) {
            // Also remove associated crop assignments
            this.farmerCrops = this.farmerCrops.filter(fc => fc.farmerId !== id);
            this.farmers.splice(index, 1);
            this.saveToLocalStorage();
            return true;
        }
        return false;
    }

    getFarmer(id) {
        return this.farmers.find(f => f.id === id);
    }

    getAllFarmers() {
        return this.farmers;
    }

    // Crop CRUD operations
    addCrop(cropData) {
        const newCrop = {
            id: this.crops.length > 0 ? Math.max(...this.crops.map(c => c.id)) + 1 : 1,
            ...cropData
        };
        this.crops.push(newCrop);
        this.saveToLocalStorage();
        return newCrop;
    }

    getAllCrops() {
        return this.crops;
    }

    // Farmer-Crop relationship operations
    assignCropToFarmer(farmerId, cropId, assignmentData) {
        const assignment = {
            id: this.farmerCrops.length > 0 ? Math.max(...this.farmerCrops.map(fc => fc.id)) + 1 : 1,
            farmerId,
            cropId,
            plantedDate: assignmentData.plantedDate || new Date().toISOString().split('T')[0],
            expectedHarvest: assignmentData.expectedHarvest || '',
            status: assignmentData.status || 'planned'
        };
        this.farmerCrops.push(assignment);
        this.saveToLocalStorage();
        return assignment;
    }

    removeCropFromFarmer(farmerId, cropId) {
        const index = this.farmerCrops.findIndex(fc => fc.farmerId === farmerId && fc.cropId === cropId);
        if (index !== -1) {
            this.farmerCrops.splice(index, 1);
            this.saveToLocalStorage();
            return true;
        }
        return false;
    }

    getFarmerCrops(farmerId) {
        return this.farmerCrops
            .filter(fc => fc.farmerId === farmerId)
            .map(fc => ({
                ...fc,
                crop: this.crops.find(c => c.id === fc.cropId),
                farmer: this.farmers.find(f => f.id === fc.farmerId)
            }));
    }

    getFarmerWithCrops(farmerId) {
        const farmer = this.getFarmer(farmerId);
        if (farmer) {
            const crops = this.getFarmerCrops(farmerId);
            return { ...farmer, crops };
        }
        return null;
    }

    // Analytics and reporting
    getFarmersByCrop(cropId) {
        return this.farmerCrops
            .filter(fc => fc.cropId === cropId)
            .map(fc => ({
                ...fc,
                farmer: this.farmers.find(f => f.id === fc.farmerId),
                crop: this.crops.find(c => c.id === fc.cropId)
            }));
    }

    getStatistics() {
        return {
            totalFarmers: this.farmers.length,
            activeFarmers: this.farmers.filter(f => f.status === 'active').length,
            totalCrops: this.crops.length,
            totalAssignments: this.farmerCrops.length,
            cropsByCategory: this.crops.reduce((acc, crop) => {
                acc[crop.category] = (acc[crop.category] || 0) + 1;
                return acc;
            }, {})
        };
    }
}

// Initialize database
const farmDB = new FarmDatabase();

// Make database globally available
window.farmDB = farmDB;
