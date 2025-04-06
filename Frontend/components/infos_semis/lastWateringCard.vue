<template>
    <div class="stat-card">
        <h4>Dernier arrosage</h4>
        <div v-if="loading" class="loading-indicator">Chargement...</div>
        <template v-else>
            <div class="stat-value">{{ lastWateredText }}</div>
            <div class="last-watered-info" v-if="lastWateredAmount">{{ lastWateredAmount }}</div>
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
    }
});

const { apiBase, getHeaders, checkAuth } = useApi();
const loading = ref(false);
const error = ref(null);
const plantData = ref(null);
const wateringHistory = ref([]);

// Format time function
const formatTime = (dateString) => {
    if (!dateString) return '';
    
    try {
        const date = new Date(dateString);
        return date.toLocaleTimeString('fr-FR', {
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (e) {
        console.error('Error formatting time:', e);
        return '';
    }
};

const lastWateredText = computed(() => {
    if (!plantData.value || !plantData.value.dernier_arrosage) return 'Jamais';
    
    const lastWatering = new Date(plantData.value.dernier_arrosage);
    const now = new Date();
    
    const diffMs = now - lastWatering;
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
    
    if (diffMins < 1) return 'À l\'instant';
    if (diffMins === 1) return 'Il y a 1 minute';
    if (diffMins < 60) return `Il y a ${diffMins} minutes`;
    
    if (diffHrs === 1) return 'Il y a 1 heure';
    if (diffHrs < 24) return `Il y a ${diffHrs} heures`;
    
    const diffDays = Math.floor(diffHrs / 24);
    if (diffDays === 1) return 'Il y a 1 jour';
    return `Il y a ${diffDays} jours`;
});

const lastWateredAmount = computed(() => {
    if (!wateringHistory.value || wateringHistory.value.length === 0) return null;
    
    const lastWatering = wateringHistory.value[0]; // Assuming sorted newest first
    const amount = lastWatering.amount || lastWatering.quantite_eau_ml;
    const dateTime = lastWatering.dateTime || lastWatering.date_arrosage;
    
    return `${formatTime(dateTime)} - ${amount} ml`;
});

const fetchData = async () => {
    if (!props.plantId) return;
    
    loading.value = true;
    error.value = null;
    
    try {
        checkAuth();
        
        // Fetch plant data to get dernier_arrosage
        const plantResponse = await $fetch(`${apiBase}/plant/semis/${props.plantId}`, {
            headers: getHeaders()
        });
        
        plantData.value = plantResponse;
        
        // Fetch watering history to get amount data
        const historyResponse = await $fetch(`${apiBase}/plant/arrosages/${props.plantId}`, {
            headers: getHeaders()
        });
        
        // Sort by date (newest first)
        wateringHistory.value = (historyResponse || [])
            .sort((a, b) => {
                const dateA = new Date(a.dateTime || a.date_arrosage);
                const dateB = new Date(b.dateTime || b.date_arrosage);
                return dateB - dateA;
            });
        
    } catch (err) {
        console.error('Error fetching last watering data:', err);
        error.value = err.message;
    } finally {
        loading.value = false;
    }
};

// Watch for changes to plantId prop
watch(() => props.plantId, (newId) => {
    if (newId) {
        fetchData();
    } else {
        plantData.value = null;
        wateringHistory.value = [];
    }
});

// Initial fetch on mount if plantId is provided
onMounted(() => {
    if (props.plantId) {
        fetchData();
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

.last-watered-info {
    color: #666;
    font-size: 0.9rem;
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
