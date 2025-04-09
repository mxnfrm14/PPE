<template>
    <div class="watering-timeline">
        <div class="schedule-header">
            <h4>Historique d'arrosage</h4>
            <div class="button-group">
                <button class="manual-water-btn" @click="$emit('openWateringPopup')">
                    Programmer un arrosage
                </button>
                <button class="manual-water-btn" @click="waterNow" :disabled="isWatering">
                    {{ isWatering ? 'Arrosage en cours...' : 'Arrosage manuel' }}
                </button>
            </div>
        </div>

        <div v-if="loading" class="loading-container">
            Chargement de l'historique...
        </div>
        <div v-else class="watering-list">
            <!-- Show when there are waterings -->
            <div v-if="history.length > 0">
                <wateringHistoryItem v-for="(entry, index) in history" :key="index"
                    :dateTime="entry.dateTime || entry.date_arrosage" :amount="entry.amount || entry.quantite_eau_ml"
                    :duration="entry.duration" :isRecent="index === 0"
                    :formattedDate="formatDate(entry.dateTime || entry.date_arrosage)"
                    :formattedTime="formatTime(entry.dateTime || entry.date_arrosage)"
                    :timeElapsed="getTimeElapsed(entry.dateTime || entry.date_arrosage)" />
            </div>

            <!-- Show when there are no waterings -->
            <div v-else class="empty-list">
                <p>Aucun historique d'arrosage disponible</p>
                <button class="schedule-btn" @click="$emit('openWateringPopup')">
                    Programmer un arrosage
                </button>
            </div>
        </div>

        <!-- Notification pour feedback d'arrosage -->
        <div v-if="wateringNotification.show" class="watering-notification" :class="wateringNotification.type">
            {{ wateringNotification.message }}
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
const isWatering = ref(false);
const wateringError = ref(null);

// État pour les notifications d'arrosage
const wateringNotification = ref({
    show: false,
    message: '',
    type: 'success'
});

// Fonction pour actualiser l'historique d'arrosage
const refreshHistory = () => {
    if (props.plantId) {
        fetchWateringHistory();
    }
};

// IMPORTANT: defineExpose doit venir APRÈS la déclaration de refreshHistory
defineExpose({ refreshHistory });

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

// Fonction pour afficher une notification temporaire
const showNotification = (message, type = 'success') => {
    wateringNotification.value = {
        show: true,
        message,
        type
    };
    
    // Masquer après 5 secondes
    setTimeout(() => {
        wateringNotification.value.show = false;
    }, 5000);
};

const waterNow = async () => {
    if (!props.plantId) {
        showNotification('Erreur: Pas de plante sélectionnée', 'error');
        return;
    }
    
    isWatering.value = true;
    wateringError.value = null;
    
    try {
        checkAuth();
        
        // Récupérer les détails de la plante pour trouver sa position
        const plantResponse = await $fetch(`${apiBase}/plant/semis/${props.plantId}`, {
            headers: getHeaders()
        });
        
        if (!plantResponse || !plantResponse.place) {
            throw new Error('Impossible de déterminer la position de la plante');
        }
        
        const place = plantResponse.place;
        
        // Récupérer l'humidité actuelle pour cette position (facultatif)
        let humidityData = null;
        try {
            const humidityResponse = await $fetch(`${apiBase}/protected/humidity/${place}`, {
                headers: getHeaders()
            });
            humidityData = humidityResponse;
            console.log('Humidité actuelle:', humidityResponse);
        } catch (humErr) {
            console.error('Erreur lors de la lecture du capteur d\'humidité:', humErr);
            // Continuer quand même, car on veut arroser même si la lecture du capteur échoue
        }
        
        // Déclencher l'arrosage immédiat
        const wateringResponse = await $fetch(`${apiBase}/plant/watering/now`, {
            method: 'POST',
            body: {
                plantId: props.plantId,
                position: place,
                duration: 5 // Durée par défaut: 5 minutes
            },
            headers: getHeaders()
        });
        
        console.log('Réponse arrosage:', wateringResponse);
        
        // Afficher un message de succès
        let successMessage = `Arrosage manuel déclenché pour la plante en position ${place}`;
        if (humidityData && humidityData.humidity !== null) {
            successMessage += `. Humidité avant arrosage: ${humidityData.humidity}%`;
        }
        
        showNotification(successMessage, 'success');
        
        // Actualiser l'historique d'arrosage après un court délai
        setTimeout(() => {
            fetchWateringHistory();
        }, 2000);
        
    } catch (err) {
        console.error('Erreur lors du déclenchement de l\'arrosage:', err);
        wateringError.value = err.message || 'Erreur lors du déclenchement de l\'arrosage';
        showNotification(`Erreur: ${wateringError.value}`, 'error');
    } finally {
        isWatering.value = false;
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

// Récupération initiale au montage si plantId est fourni
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
    position: relative;
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

.manual-water-btn:disabled {
    background-color: #90caf9;
    cursor: not-allowed;
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

/* Notification d'arrosage */
.watering-notification {
    position: absolute;
    bottom: 1rem;
    right: 1rem;
    padding: 0.8rem 1.2rem;
    border-radius: 0.5rem;
    color: white;
    font-weight: 500;
    max-width: 90%;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    z-index: 5;
    animation: fadeIn 0.3s, fadeOut 0.3s 4.7s;
}

.watering-notification.success {
    background-color: #4caf50;
}

.watering-notification.error {
    background-color: #f44336;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeOut {
    from { opacity: 1; transform: translateY(0); }
    to { opacity: 0; transform: translateY(20px); }
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

.button-group {
    display: flex;
    gap: 10px;
}

@media (max-width: 768px) {
    .button-group {
        flex-direction: column;
    }
}
</style>