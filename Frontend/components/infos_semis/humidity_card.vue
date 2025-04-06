<template>
    <div class="stat-card">
        <h4>Humidité actuelle</h4>
        <div v-if="loading" class="loading-indicator">Chargement...</div>
        <template v-else>
            <div class="stat-value">{{ humidityLevel }}%</div>
            <div class="stat-chart">
                <div class="progress-bar">
                    <div class="progress" :style="{ width: humidityLevel + '%' }"></div>
                </div>
            </div>
        </template>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';

const props = defineProps({
    plantId: {
        type: String,
        default: null
    },
    defaultHumidity: {
        type: Number,
        default: 60
    }
});

const { apiBase, getHeaders, checkAuth } = useApi();
const loading = ref(false);
const error = ref(null);
const plantData = ref(null);
const plantInfo = ref(null);
const humidityLevel = computed(() => {
    // Use the actual humidity level from the database if available
    if (plantData.value && plantData.value.txHumidMesure !== undefined) {
        return plantData.value.txHumidMesure;
    }
    
    // Fallback to recommended level if available
    if (plantInfo.value && plantInfo.value.recommandedHumidityLevel) {
        return plantInfo.value.recommandedHumidityLevel;
    }
    
    // Default fallback value
    return props.defaultHumidity;
});

const fetchHumidityData = async () => {
    if (!props.plantId) return;
    
    loading.value = true;
    error.value = null;
    
    try {
        checkAuth();
        
        // Get plant data for actual humidity
        const response = await $fetch(`${apiBase}/plant/semis/${props.plantId}`, {
            headers: getHeaders()
        });
        
        plantData.value = response;
        
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

// Watch for changes to plantId prop
watch(() => props.plantId, (newId) => {
    if (newId) {
        fetchHumidityData();
    } else {
        plantData.value = null;
        plantInfo.value = null;
    }
});

// Initial fetch on mount if plantId is provided
onMounted(() => {
    if (props.plantId) {
        fetchHumidityData();
    }
});
</script>

<style scoped>
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
</style>
