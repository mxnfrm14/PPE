<template>
    <div class="infos">
        <!-- Loading state -->
        <div v-if="isLoading" class="loading">
            Chargement des informations...
        </div>
        
        <!-- Error state -->
        <div v-else-if="error" class="error-message">
            {{ error }}
        </div>
        
        <!-- Display info when a plant is selected and loaded -->
        <div v-else-if="props.selectedPlantId && plant" class="info-card">
            <div class="info-header">
                <h3>{{ plant.nom }}</h3>
                
                <!-- Edit and Delete buttons -->
                <div class="action-buttons">
                    <button class="action-btn edit-btn" @click="handleEdit" title="Modifier">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                    </button>
                    <button class="action-btn delete-btn" @click="handleDelete" title="Supprimer">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M3 6h18"></path>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path>
                            <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                            <line x1="10" y1="11" x2="10" y2="17"></line>
                            <line x1="14" y1="11" x2="14" y2="17"></line>
                        </svg>
                    </button>
                </div>
            </div>
            
            <div class="text-info">
                <!-- Stats cards for humidity and last watering -->
                <div class="stats-container">
                    <HumidityCard :plantId="props.selectedPlantId" />
                    <LastWateringCard :plantId="props.selectedPlantId" />
                </div>
                
                <!-- Additional info from infos collection -->
                <div class="info-section">
                    <div class="info-row">
                        <span class="info-label">Date de plantation:</span>
                        <span class="info-value">{{ formatDate(plant.date_plantation) }}</span>
                    </div>
                
                    <template v-if="plantInfo">
                        <div class="info-row">
                            <span class="info-label">Période de semis:</span>
                            <span class="info-value">{{ plantInfo.semisStartPeriod }} à {{ plantInfo.semisEndPeriod }}</span>
                        </div>
                        
                        <div class="info-row">
                            <span class="info-label">Durée de germination:</span>
                            <span class="info-value">{{ plantInfo.growingDurationLow }} à {{ plantInfo.growingDurationHigh }} jours</span>
                        </div>
                        
                        <div class="info-row">
                            <span class="info-label">Température idéale:</span>
                            <span class="info-value">{{ plantInfo.recommandedTemperatureLow }}°C - {{ plantInfo.recommandedTemperatureHigh }}°C</span>
                        </div>
                        
                        <div class="info-row">
                            <span class="info-label">Méthode recommandée:</span>
                            <span class="info-value">
                                <div v-for="(method, index) in plantInfo.recommandedMethods" :key="index">
                                    {{ method }}
                                </div>
                            </span>
                        </div>
                        
                        <div class="info-row">
                            <span class="info-label">Sol:</span>
                            <span class="info-value">{{ plantInfo.cultureCondition?.solType || '' }}</span>
                        </div>
                        
                        <div class="info-row" v-if="plantInfo.cultureCondition?.externCondition">
                            <span class="info-label">Conditions externes:</span>
                            <span class="info-value">{{ plantInfo.cultureCondition.externCondition }}</span>
                        </div>
                        
                        <div class="info-row">
                            <span class="info-label">Besoin en eau:</span>
                            <span class="info-value">{{ plantInfo.cultureCondition?.waterNeed || '' }}</span>
                        </div>
                        
                        <div class="info-row">
                            <span class="info-label">Taux humidité recommandé:</span>
                            <span class="info-value">{{ plantInfo.recommandedHumidityLevel }}%</span>
                        </div>
                    </template>
                </div>
                
                <!-- Full-width watering history -->
                <div class="watering-container">
                    <WateringHistory 
                        ref="wateringHistoryRef"
                        :plantId="props.selectedPlantId" 
                        @openWateringPopup="openWateringPopup" 
                    />
                </div>
            </div>
        </div>
        <div v-else class="no-selection">
            <p>Veuillez sélectionner un semis pour voir les informations détaillées</p>
        </div>
        
        <!-- Watering popup -->
        <WateringForm 
            :showPopup="showWateringPopup"
            :plantId="props.selectedPlantId"
            @close="showWateringPopup = false"
            @success="handleWateringSuccess"
            @error="handleWateringError"
        />
        
        <!-- Notification toast -->
        <div v-if="showNotification" class="notification" :class="notificationType">
            {{ notificationMessage }}
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';
import HumidityCard from './infos_semis/humidity_card.vue';
import LastWateringCard from './infos_semis/lastWateringCard.vue';
import WateringHistory from './infos_semis/wateringHistory.vue';
import WateringForm from './infos_semis/wateringForm.vue';

// Props to receive selected plant ID
const props = defineProps({
    selectedPlantId: {
        type: String,
        default: null
    }
});

// Define emits for edit and delete actions
const emit = defineEmits(['editPlant', 'deletePlant']);

// API utilities
const { apiBase, getHeaders, checkAuth } = useApi();

// Reactive data
const plant = ref(null);
const plantInfo = ref(null);
const isLoading = ref(false);
const error = ref(null);
const wateringHistoryRef = ref(null);

// Popup state
const showWateringPopup = ref(false);
const showNotification = ref(false);
const notificationMessage = ref('');
const notificationType = ref('success');

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

// Watch for changes to selected plant ID
watch(() => props.selectedPlantId, (newId) => {
    if (newId) {
        fetchPlantDetails(newId);
    } else {
        plant.value = null;
    }
});

// Fetch plant details from API
const fetchPlantDetails = async (id) => {
    isLoading.value = true;
    error.value = null;
    
    try {
        checkAuth();
        
        // Fetch plant data
        const response = await $fetch(`${apiBase}/plant/semis/${id}`, {
            headers: getHeaders()
        });
        
        plant.value = response;
        
        // Fetch plant info from infos collection
        try {
            const infoResponse = await $fetch(`${apiBase}/plant/infos/carotte`, {
                headers: getHeaders()
            });
            
            plantInfo.value = infoResponse;
        } catch (infoErr) {
            console.error('Error fetching plant info:', infoErr);
            plantInfo.value = null;
        }
    } catch (err) {
        console.error('Error fetching plant details:', err);
        error.value = err.message || "Impossible de charger les détails du semis";
    } finally {
        isLoading.value = false;
    }
};

// Open watering popup
const openWateringPopup = () => {
    showWateringPopup.value = true;
};

// Handle watering success
const handleWateringSuccess = (result) => {
    showWateringPopup.value = false;
    notificationMessage.value = result.message || "Arrosage enregistré avec succès!";
    notificationType.value = "success";
    showNotification.value = true;
    
    // Refresh watering history
    if (wateringHistoryRef.value) {
        wateringHistoryRef.value.refreshHistory();
    }
    
    // Refresh plant details
    if (props.selectedPlantId) {
        fetchPlantDetails(props.selectedPlantId);
    }
    
    // Auto-hide notification after 3 seconds
    setTimeout(() => {
        showNotification.value = false;
    }, 3000);
};

// Handle watering error
const handleWateringError = (errorMessage) => {
    notificationMessage.value = errorMessage || "Erreur lors de l'ajout de l'arrosage";
    notificationType.value = "error";
    showNotification.value = true;
    
    // Auto-hide notification after 3 seconds
    setTimeout(() => {
        showNotification.value = false;
    }, 3000);
};

// Function to handle edit button click
const handleEdit = () => {
    if (plant.value) {
        // Emit event to parent component
        emit('editPlant', plant.value);
    }
};

// Function to handle delete button click
const handleDelete = () => {
    if (plant.value) {
        // Emit event to parent component
        emit('deletePlant', plant.value);
    }
};

// Load data on mount if a plant is selected
onMounted(() => {
    if (props.selectedPlantId) {
        fetchPlantDetails(props.selectedPlantId);
    }
});
</script>

<style scoped>
.infos {
    gap: 0.05rem;
    margin-bottom: 1.5rem;
    border-radius: 1.6rem;
    position: relative;
}

.info-card {
    background-color: white;
    border-radius: 0.8rem;
    overflow: hidden;
    margin: 0.6rem;
    box-shadow: 1px 3px 3px 1px #d8d8d8;
    padding: 1rem;
}

.info-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #f0f0f0;
    margin-bottom: 1rem;
}

.info-header h3 {
    font-family: 'Aeonik-Medium', sans-serif;
    color: #333;
    margin-bottom: 0;
    font-size: 1.2rem;
}

.action-buttons {
    display: flex;
    gap: 0.5rem;
}

.action-btn {
    background: none;
    border: none;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: background-color 0.2s;
}

.edit-btn {
    color: #3498db;
}

.delete-btn {
    color: #e74c3c;
}

.action-btn:hover {
    background-color: #f5f5f5;
}

.text-info {
    padding: 0.5rem;
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

.info-section {
    font-family: 'Aeonik-Regular', sans-serif;
    margin: 1.5rem 0;
}

.info-row {
    display: flex;
    margin-bottom: 0.7rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid #f0f0f0;
}

.info-label {
    flex: 0 0 40%;
    font-weight: 500;
    color: #95bd75;
}

.info-value {
    flex: 0 0 60%;
    color: #444;
}

.no-selection, .not-found {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
    color: #888;
    font-style: italic;
    text-align: center;
}

.loading {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
    color: #333;
}

.error-message {
    color: #f44336;
    padding: 1rem;
    background-color: #ffebee;
    border-radius: 0.5rem;
    margin: 1rem 0;
}

/* Stats cards styling */
.stats-container {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

/* Watering container */
.watering-container {
    margin-top: 2rem;
    width: 100%;
}

.notification {
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 1rem 1.5rem;
    border-radius: 0.5rem;
    color: white;
    font-weight: 500;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 1100;
    animation: fadeIn 0.3s, fadeOut 0.3s 2.7s;
}

.notification.success {
    background-color: #4caf50;
}

.notification.error {
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
    .stats-container {
        flex-direction: column;
    }
    
    .info-row {
        flex-direction: column;
    }
    
    .info-label, .info-value {
        flex: 1 1 100%;
    }
    
    .info-label {
        margin-bottom: 0.2rem;
    }
}
</style>