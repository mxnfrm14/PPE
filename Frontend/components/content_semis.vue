<template>
    <div class="content-container">
        <div v-if="currentView === 'arrosage'" class="view-content">
            <h3>Gestion de l'Arrosage des Semis</h3>
            
            <!-- Plant selection dropdown -->
            <div class="plant-selector">
                <label for="plant-select">Sélectionner une plante:</label>
                <select id="plant-select" v-model="selectedPlant">
                    <option value="tomates">Tomates</option>
                    <option value="basilic">Basilic</option>
                    <option value="laitue">Laitue</option>
                </select>
            </div>
            
            <div class="stats-container">
                <div class="stat-card">
                    <h4>Humidité actuelle</h4>
                    <div class="stat-value">{{ plantData[selectedPlant].humidity }}%</div>
                    <div class="stat-chart">
                        <div class="progress-bar">
                            <div class="progress" :style="{ width: plantData[selectedPlant].humidity + '%' }"></div>
                        </div>
                    </div>
                </div>
                <div class="stat-card">
                    <h4>Dernier arrosage</h4>
                    <div class="stat-value">{{ plantData[selectedPlant].lastWatered }}</div>
                    <div class="last-watered-info">{{ plantData[selectedPlant].waterAmount }}</div>
                </div>
            </div>
            <div class="schedule-container">
                <div class="schedule-header">
                    <h4>Planning d'arrosage</h4>
                    <!-- Manual water button -->
                    <button class="manual-water-btn" @click="waterPlantManually">
                        Arroser manuellement
                    </button>
                </div>
                <ul class="schedule-list">
                    <li class="schedule-item" v-for="(schedule, index) in plantData[selectedPlant].schedules" :key="index">
                        <div class="schedule-time">{{ schedule.time }}</div>
                        <div class="schedule-action">{{ schedule.action }}</div>
                    </li>
                </ul>
            </div>
        </div>

        <div v-else-if="currentView === 'temperature'" class="view-content">
            <h3>Gestion de la Température</h3>
            <div class="stats-container single-card">
                <div class="stat-card">
                    <h4>Température actuelle</h4>
                    <div class="stat-value">24°C</div>
                    <div class="temp-range">
                        <span>Min: 18°C</span>
                        <span>Max: 28°C</span>
                    </div>
                </div>
            </div>
            <div class="temperature-chart">
                <h4>Variations sur 24h</h4>
                <div class="chart-placeholder">
                    Graphique des variations de température
                </div>
            </div>
        </div>

        <div v-else-if="currentView === 'plantations'" class="view-content">
            <h3>Gestion des Plantations</h3>
            <div class="plants-grid">
                <div class="plant-card" v-for="(plant, index) in plants" :key="index">
                    <div class="plant-header">{{ plant.name }}</div>
                    <div class="plant-info">
                        <p>Semis le: {{ plant.plantedDate }}</p>
                        <p>Jours restants: {{ plant.daysRemaining }}</p>
                        <div class="growth-indicator">
                            <div class="growth-bar">
                                <div class="growth-progress" :style="{ width: plant.growth + '%' }"></div>
                            </div>
                            <span>{{ plant.growth }}%</span>
                        </div>
                        <button class="edit-plant-btn" @click="editPlant(index)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
                            </svg>
                            Modifier
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

// Default view is arrosage
const currentView = ref('arrosage');
const selectedPlant = ref('tomates');

// Mock plant data for watering section
const plantData = reactive({
    tomates: {
        humidity: 65,
        lastWatered: 'Il y a 2 heures',
        waterAmount: '10:15 - 250ml',
        schedules: [
            { time: '08:00', action: 'Arrosage automatique - 300ml' },
            { time: '16:00', action: 'Arrosage automatique - 300ml' }
        ]
    },
    basilic: {
        humidity: 78,
        lastWatered: 'Il y a 1 heure',
        waterAmount: '11:30 - 150ml',
        schedules: [
            { time: '09:00', action: 'Arrosage automatique - 150ml' },
            { time: '17:00', action: 'Arrosage automatique - 150ml' }
        ]
    },
    laitue: {
        humidity: 42,
        lastWatered: 'Il y a 4 heures',
        waterAmount: '08:15 - 200ml',
        schedules: [
            { time: '07:30', action: 'Arrosage automatique - 200ml' },
            { time: '15:30', action: 'Arrosage automatique - 200ml' }
        ]
    }
});

// Plants for plantation management section
const plants = reactive([
    {
        name: 'Tomates',
        plantedDate: '15 février',
        daysRemaining: 12,
        growth: 65
    },
    {
        name: 'Basilic',
        plantedDate: '20 février',
        daysRemaining: 8,
        growth: 80
    },
    {
        name: 'Laitue',
        plantedDate: '10 février',
        daysRemaining: 5,
        growth: 90
    }
]);

// Function to water plant manually
const waterPlantManually = () => {
    // Here you would call your API to trigger watering
    alert(`Arrosage manuel de ${selectedPlant.value} déclenché`);
    
    // Update last watered time
    const now = new Date();
    const timeString = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;
    
    plantData[selectedPlant.value].lastWatered = 'À l\'instant';
    plantData[selectedPlant.value].waterAmount = `${timeString} - 200ml`;
    
    // Update humidity level
    plantData[selectedPlant.value].humidity = Math.min(95, plantData[selectedPlant.value].humidity + 15);
};

// Function to edit plant details
const editPlant = (index) => {
    alert(`Modification des informations pour: ${plants[index].name}`);
    // Here you would open a modal or navigate to edit screen
};

// Export the method to change views
defineExpose({
    setView: (view) => {
        currentView.value = view;
    }
});
</script>

<style scoped>
.content-container {
    background-color: white;
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    margin-top: 1rem;
    min-height: 400px;
}

h3 {
    font-family: 'Aeonik-Medium', sans-serif;
    color: #333;
    margin-bottom: 1.5rem;
    font-size: 1.2rem;
}

h4 {
    font-family: 'Aeonik-Medium', sans-serif;
    color: #555;
    margin-bottom: 0.5rem;
    font-size: 1rem;
}

.plant-selector {
    margin-bottom: 1.5rem;
}

.plant-selector label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #333;
}

.plant-selector select {
    width: 100%;
    max-width: 300px;
    padding: 0.5rem;
    border-radius: 0.5rem;
    border: 1px solid #ddd;
    font-size: 1rem;
    background-color: #f9f9f9;
}

.stats-container {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stats-container.single-card {
    max-width: 300px;
}

.stat-card {
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    padding: 1rem;
    flex: 1;
}

.stat-value {
    font-size: 1.8rem;
    font-weight: bold;
    color: #333;
    margin: 0.5rem 0;
}

.progress-bar {
    width: 100%;
    height: 0.6rem;
    background-color: #e0e0e0;
    border-radius: 0.3rem;
    overflow: hidden;
    margin-top: 0.5rem;
}

.progress {
    height: 100%;
    background-color: #95bd75;
    border-radius: 0.3rem;
}

.last-watered-info {
    color: #666;
    font-size: 0.9rem;
}

.schedule-container {
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    padding: 1rem;
}

.schedule-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.manual-water-btn {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.manual-water-btn:hover {
    background-color: #2980b9;
}

.schedule-list {
    list-style-type: none;
    padding: 0;
}

.schedule-item {
    display: flex;
    padding: 0.8rem 0;
    border-bottom: 1px solid #eee;
}

.schedule-time {
    font-weight: bold;
    width: 80px;
}

.schedule-action {
    flex: 1;
}

.temp-range {
    display: flex;
    justify-content: space-between;
    color: #666;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

.temperature-chart {
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    padding: 1rem;
    margin-top: 1rem;
}

.chart-placeholder {
    height: 150px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px dashed #ccc;
    border-radius: 0.5rem;
    color: #888;
    margin-top: 1rem;
}

.plants-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.plant-card {
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    overflow: hidden;
}

.plant-header {
    background-color: #95bd75;
    color: white;
    font-weight: bold;
    padding: 0.8rem 1rem;
}

.plant-info {
    padding: 1rem;
}

.plant-info p {
    margin: 0.3rem 0;
    color: #444;
}

.growth-indicator {
    margin-top: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.growth-bar {
    flex: 1;
    height: 0.5rem;
    background-color: #e0e0e0;
    border-radius: 0.25rem;
    overflow: hidden;
}

.growth-progress {
    height: 100%;
    background-color: #95bd75;
}

.edit-plant-btn {
    margin-top: 1rem;
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 0.4rem;
    padding: 0.5rem 0.8rem;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.3rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.edit-plant-btn:hover {
    background-color: #e4e4e4;
}

.edit-plant-btn svg {
    width: 14px;
    height: 14px;
}

@media (max-width: 768px) {
    .stats-container {
        flex-direction: column;
    }
    
    .schedule-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
    
    .plants-grid {
        grid-template-columns: 1fr;
    }
}
</style>