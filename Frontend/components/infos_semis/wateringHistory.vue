<template>
    <div class="watering-timeline">
        <div class="schedule-header">
            <h4>Historique d'arrosage</h4>
            <button class="manual-water-btn" @click="$emit('openWateringPopup')">
                Arroser manuellement
            </button>
        </div>

        <div v-if="loading" class="loading-container">
            Chargement de l'historique...
        </div>
        <div v-else class="watering-list">
            <!-- Show when there are waterings -->
            <div v-if="history.length > 0">
                <wateringHistoryItem
                    v-for="(entry, index) in history"
                    :key="index"
                    :dateTime="entry.dateTime || entry.date_arrosage"
                    :amount="entry.amount || entry.quantite_eau_ml"
                    :duration="entry.duration"
                    :isRecent="index === 0"
                    :formattedDate="formatDate(entry.dateTime || entry.date_arrosage)"
                    :formattedTime="formatTime(entry.dateTime || entry.date_arrosage)"
                    :timeElapsed="getTimeElapsed(entry.dateTime || entry.date_arrosage)"
                />
            </div>
            
            <!-- Show when there are no waterings -->
            <div v-else class="empty-list">
                <p>Aucun historique d'arrosage disponible</p>
                <button class="schedule-btn" @click="$emit('openWateringPopup')">
                    Programmer un arrosage
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';
import wateringHistoryItem from './wateringHistoryItem.vue';

const props = defineProps({
    plantId: {
        type: String,
        required: true
    }
});

const emit = defineEmits(['openWateringPopup']);

const { apiBase, getHeaders, checkAuth } = useApi();
const history = ref([]);
const loading = ref(false);
const error = ref(null);

// Format date function
const formatDate = (dateString) => {
    if (!dateString) return 'Non défini';
    
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('fr-FR', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    } catch (e) {
        console.error('Error formatting date:', e);
        return dateString;
    }
};

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

// Calculate time elapsed from a given date
const getTimeElapsed = (dateString) => {
    if (!dateString) return '';
    
    try {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        
        // Convert to appropriate time units
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        const diffHrs = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        
        if (diffDays > 0) {
            return diffDays === 1 ? 'Il y a 1 jour' : `Il y a ${diffDays} jours`;
        } else if (diffHrs > 0) {
            return diffHrs === 1 ? 'Il y a 1 heure' : `Il y a ${diffHrs} heures`;
        } else {
            const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
            return diffMins <= 1 ? 'Il y a quelques minutes' : `Il y a ${diffMins} minutes`;
        }
    } catch (e) {
        console.error('Error calculating time elapsed:', e);
        return '';
    }
};

const fetchWateringHistory = async () => {
    if (!props.plantId) return;
    
    loading.value = true;
    error.value = null;
    
    try {
        checkAuth();
        
        const response = await $fetch(`${apiBase}/plant/arrosages/${props.plantId}`, {
            headers: getHeaders()
        });
        console.log('Watering history response:', response);
        // Sort the watering history by date (newest first)
        history.value = (response || [])
            .sort((a, b) => {
                const dateA = new Date(a.dateTime || a.date_arrosage);
                const dateB = new Date(b.dateTime || b.date_arrosage);
                return dateB - dateA; // Sort descending (newest first)
            });
    } catch (err) {
        console.error('Error fetching watering history:', err);
        error.value = err.message;
        history.value = [];
    } finally {
        loading.value = false;
    }
};

// Watch for changes to plantId prop
watch(() => props.plantId, (newId) => {
    if (newId) {
        fetchWateringHistory();
    } else {
        history.value = [];
    }
});

// Expose method to refresh history data
const refreshHistory = () => {
    if (props.plantId) {
        fetchWateringHistory();
    }
};

// Make the method available to parent component
defineExpose({ refreshHistory });

// Initial fetch on mount if plantId is provided
onMounted(() => {
    if (props.plantId) {
        fetchWateringHistory();
    }
});
</script>

<style scoped>
.watering-timeline {
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    padding: 1rem;
    width: 100%;
    min-height: 300px;
}

.schedule-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    border-bottom: 1px solid #eee;
    padding-bottom: 0.5rem;
}

h4 {
    font-family: 'Aeonik-Medium', sans-serif;
    color: #555;
    margin-bottom: 0.5rem;
    font-size: 1rem;
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

.watering-list {
    min-height: 200px;
}

.empty-list {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #888;
    font-style: italic;
    padding: 2rem;
    text-align: center;
    gap: 1rem;
    min-height: 200px;
}

.schedule-btn {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.schedule-btn:hover {
    background-color: #2980b9;
}

@media (max-width: 768px) {
    .schedule-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
}

.loading-container {
    min-height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #888;
    font-style: italic;
}
</style>
