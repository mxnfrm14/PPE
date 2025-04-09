<template>
    <div class="stat-card">
        <h4>Humidité actuelle</h4>
        <button 
            class="refresh-button" 
            @click="fetchHumidityData" 
            :disabled="loading" 
            title="Rafraîchir les données"
        >
            <span class="refresh-icon" :class="{ 'refreshing': loading }">↻</span>
        </button>
        <div v-if="loading" class="loading-indicator">Chargement...</div>
        <template v-else>
            <div class="stat-value">{{ humidityLevel }}%</div>
            <div v-if="sensorReading" class="sensor-info" :class="sensorReading.status">
                <span v-if="sensorReading.status === 'success'" class="live-indicator">●</span>
                <span>{{ sensorStatusText }}</span>
            </div>
            <div class="stat-chart">
                <div class="progress-bar">
                    <div class="progress" :style="{ width: humidityLevel + '%', backgroundColor: humidityColor }"></div>
                </div>
            </div>
            <div class="timestamp" v-if="sensorReading && sensorReading.timestamp">
                Dernière mise à jour: {{ formatTimestamp(sensorReading.timestamp) }}
            </div>
        </template>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useApi } from '~/composables/useApi';

const props = defineProps({
    plantId: {
        type: String,
        default: null
    },
    defaultHumidity: {
        type: Number,
        default: 60
    },
    refreshInterval: {
        type: Number,
        default: 60000 // 1 minute
    }
});

const { apiBase, getHeaders, checkAuth } = useApi();
const loading = ref(false);
const error = ref(null);
const plantData = ref(null);
const plantInfo = ref(null);
const sensorReading = ref(null);
let refreshTimer = null;

// Compute the humidity level to display
const humidityLevel = computed(() => {
    // If we have a sensor reading, use that first
    if (sensorReading.value && sensorReading.value.humidity !== undefined) {
        return Math.round(sensorReading.value.humidity);
    }
    
    // Otherwise fall back to database value
    if (plantData.value && plantData.value.txHumidMesure !== undefined) {
        return plantData.value.txHumidMesure;
    }
    
    // Fall back to recommended level if available
    if (plantInfo.value && plantInfo.value.recommandedHumidityLevel) {
        return plantInfo.value.recommandedHumidityLevel;
    }
    
    // Default fallback value
    return props.defaultHumidity;
});

// Format timestamp to readable format
const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';
    
    try {
        // Replace space with T to handle the format correctly
        const date = new Date(timestamp.replace(' ', 'T'));
        return new Intl.DateTimeFormat('fr-FR', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            day: '2-digit',
            month: '2-digit'
        }).format(date);
    } catch (e) {
        console.error('Error formatting timestamp:', e);
        return timestamp;
    }
};

// Compute display text for sensor status
const sensorStatusText = computed(() => {
    if (!sensorReading.value) return '';
    
    switch (sensorReading.value.status) {
        case 'success':
            return 'Capteur en direct';
        case 'cached':
            return 'Données en cache';
        case 'error':
            return `Erreur: ${sensorReading.value.error || 'Capteur non disponible'}`;
        default:
            return '';
    }
});

// Compute color based on humidity level
const humidityColor = computed(() => {
    const level = humidityLevel.value;
    
    if (level < 20) return '#e74c3c'; // Very dry - red
    if (level < 40) return '#e67e22'; // Dry - orange
    if (level < 60) return '#f1c40f'; // Getting dry - yellow
    if (level < 80) return '#2ecc71'; // Good - green
    return '#3498db';                 // Very wet - blue
});

const fetchHumidityData = async () => {
    if (!props.plantId) return;
    
    loading.value = true;
    error.value = null;
    
    try {
        checkAuth();
        
        // Get plant data to know the position
        const response = await $fetch(`${apiBase}/plant/semis/${props.plantId}`, {
            headers: getHeaders()
        });
        
        plantData.value = response;
        const place = response.place;
        
        // Only fetch from sensor if the place has a sensor
        const sensorPlaces = [5, 8, 11]; // Places that have sensors
        
        if (sensorPlaces.includes(place)) {
            try {
                // Fetch real-time humidity from the sensor
                const sensorResponse = await $fetch(`${apiBase}/protected/humidity/${place}`, {
                    headers: getHeaders()
                });
                
                sensorReading.value = sensorResponse;
                console.log(`Sensor reading for place ${place}:`, sensorResponse);
            } catch (sensorErr) {
                console.error('Error fetching sensor data:', sensorErr);
                // Don't set error here, just continue with database value
                sensorReading.value = {
                    status: 'error',
                    error: sensorErr.message || 'Erreur de lecture du capteur'
                };
            }
        } else {
            console.log(`Place ${place} does not have a humidity sensor, using database value`);
            sensorReading.value = null;
        }
        
        // Try to get recommended humidity from plant info
        try {
            // Note: In a real app, you'd use the plant type rather than hardcoding "carotte"
            const infoResponse = await $fetch(`${apiBase}/plant/infos/carotte`, {
                headers: getHeaders()
            });
            plantInfo.value = infoResponse;
        } catch (infoErr) {
            console.error('Error fetching plant info for humidity:', infoErr);
        }
    } catch (err) {
        console.error('Error fetching humidity data:', err);
        error.value = err.message;
    } finally {
        loading.value = false;
    }
};

// Setup auto-refresh timer
const setupRefreshTimer = () => {
    clearRefreshTimer();
    if (props.refreshInterval > 0) {
        refreshTimer = setInterval(fetchHumidityData, props.refreshInterval);
    }
};

const clearRefreshTimer = () => {
    if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = null;
    }
};

// Watch for changes to plantId prop
watch(() => props.plantId, (newId) => {
    if (newId) {
        fetchHumidityData();
        setupRefreshTimer();
    } else {
        plantData.value = null;
        plantInfo.value = null;
        sensorReading.value = null;
        clearRefreshTimer();
    }
});

// Initial fetch on mount if plantId is provided
onMounted(() => {
    if (props.plantId) {
        fetchHumidityData();
        setupRefreshTimer();
    }
});

// Clean up on unmount
onUnmounted(() => {
    clearRefreshTimer();
});
</script>

<style scoped>
.stat-card {
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    padding: 1rem;
    flex: 1;
    position: relative; /* Added to position the refresh button */
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
    transition: width 0.3s ease-out;
}

.sensor-info {
    font-size: 0.8rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

.sensor-info.success {
    color: #2ecc71;
}

.sensor-info.cached {
    color: #f39c12;
}

.sensor-info.error {
    color: #e74c3c;
}

.live-indicator {
    font-size: 1rem;
    animation: blink 2s infinite;
}

@keyframes blink {
    0% { opacity: 0.3; }
    50% { opacity: 1; }
    100% { opacity: 0.3; }
}

h4 {
    font-family: 'Aeonik-Medium', sans-serif;
    color: #555;
    margin-bottom: 0.5rem;
    font-size: 1rem;
}

.loading-indicator {
    height: 3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #888;
    font-style: italic;
}

.refresh-button {
    position: absolute;
    top: 0.8rem;
    right: 0.8rem;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0.3rem;
    border-radius: 50%;
    transition: background-color 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.refresh-button:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

.refresh-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.refresh-icon {
    font-size: 1.2rem;
    color: #555;
    transition: transform 0.3s ease;
}

.refresh-icon.refreshing {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.timestamp {
    font-size: 0.75rem;
    color: #777;
    margin-top: 0.5rem;
    text-align: right;
}
</style>