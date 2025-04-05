<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue';
import { useRuntimeConfig } from 'nuxt/app';
import { useAuth } from '~/composables/useAuth';

// Get the API base URL and auth token
const config = useRuntimeConfig();
const apiBase = config.public.apiBaseUrl;
const { token } = useAuth();

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

// Props to receive selected plant ID
const props = defineProps({
    selectedPlantId: {
        type: String,
        default: null
    }
});

// Reactive data
const plant = ref(null);
const plantInfo = ref(null);
const wateringHistory = ref([]);
const isLoading = ref(false);
const error = ref(null);

// Popup state
const showWateringPopup = ref(false);
const wateringForm = reactive({
    date: new Date().toISOString().split('T')[0], // Today's date in YYYY-MM-DD format
    time: new Date().toTimeString().slice(0, 5), // Current time in HH:MM format
    duration: 5, // Default duration in minutes
    amount: 200 // Default amount in ml
});
const isSubmitting = ref(false);
const showNotification = ref(false);
const notificationMessage = ref('');
const notificationType = ref('success');

// Watch for changes to selected plant ID
watch(() => props.selectedPlantId, (newId) => {
    if (newId) {
        fetchPlantDetails(newId);
        fetchWateringHistory(newId);
    } else {
        plant.value = null;
        wateringHistory.value = [];
    }
});

// Fetch plant details from API
const fetchPlantDetails = async (id) => {
    isLoading.value = true;
    error.value = null;
    
    try {
        // Check if token exists
        if (!token.value) {
            throw new Error('Vous devez être connecté pour accéder à cette page');
        }
        
        // Fetch plant data
        const response = await $fetch(`${apiBase}/plant/semis/${id}`, {
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        });
        
        console.log('Fetched plant details:', response);
        plant.value = response;
        
        // Fetch plant info from infos collection - we need to create this endpoint
        try {
            const infoResponse = await $fetch(`${apiBase}/plant/infos/carotte`, {
                headers: {
                    'Authorization': `Bearer ${token.value}`
                }
            });
            
            console.log('Fetched plant info:', infoResponse);
            plantInfo.value = infoResponse;
        } catch (infoErr) {
            console.error('Error fetching plant info:', infoErr);
            // Don't set the main error, still show plant details without info
            plantInfo.value = null;
        }
    } catch (err) {
        console.error('Error fetching plant details:', err);
        error.value = err.message || "Impossible de charger les détails du semis";
        
        // Redirect to login if unauthorized
        if (err.response?.status === 401) {
            navigateTo('/login');
        }
    } finally {
        isLoading.value = false;
    }
};

// Fetch watering history from API
const fetchWateringHistory = async (id) => {
    try {
        // Check if token exists
        if (!token.value) {
            console.error('Token missing for watering history fetch');
            return;
        }
        
        const response = await $fetch(`${apiBase}/plant/arrosages/${id}`, {
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        });
        
        console.log('Fetched watering history:', response);
        wateringHistory.value = response || [];
    } catch (err) {
        console.error('Error fetching watering history:', err);
        // We don't set the main error here to still show plant details
    }
};

// Open watering popup
const openWateringPopup = () => {
    // Reset form to defaults with current date and time
    const now = new Date();
    wateringForm.date = now.toISOString().split('T')[0];
    wateringForm.time = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    wateringForm.duration = 5;
    wateringForm.amount = 200;
    
    // Show popup
    showWateringPopup.value = true;
};

// Submit watering form
const submitWatering = async () => {
    if (!props.selectedPlantId) return;
    
    isSubmitting.value = true;
    
    try {
        // Check if token exists
        if (!token.value) {
            throw new Error('Vous devez être connecté pour effectuer cette action');
        }
        
        // Combine date and time
        const dateTime = `${wateringForm.date}T${wateringForm.time}:00`;
        
        // Prepare data for API
        const wateringData = {
            semis_id: props.selectedPlantId,  // Changed to match your DB schema
            date_arrosage: dateTime,          // Changed to match your DB schema
            quantite_eau_ml: wateringForm.amount  // Changed to match your DB schema
        };
        
        console.log('Submitting watering data:', wateringData);
        
        // Submit to API
        await $fetch(`${apiBase}/plant/arrosages`, {
            method: 'POST',
            body: wateringData,
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        });
        
        // Close popup and show success notification
        showWateringPopup.value = false;
        notificationMessage.value = "Arrosage programmé avec succès!";
        notificationType.value = "success";
        showNotification.value = true;
        
        // Refresh watering history
        fetchWateringHistory(props.selectedPlantId);
        
        // Auto-hide notification after 3 seconds
        setTimeout(() => {
            showNotification.value = false;
        }, 3000);
    } catch (err) {
        console.error('Error submitting watering:', err);
        notificationMessage.value = err.message || "Erreur lors de l'ajout de l'arrosage";
        notificationType.value = "error";
        showNotification.value = true;
        
        // Redirect to login if unauthorized
        if (err.response?.status === 401) {
            navigateTo('/login');
        }
    } finally {
        isSubmitting.value = false;
    }
};

// Helper methods for displaying humidity and watering info
const getHumidityLevel = () => {
    if (plantInfo.value && plantInfo.value.recommandedHumidityLevel) {
        // Use a random value based on recommended level (just for demonstration)
        // In a real scenario, this would come from a sensor or API
        const variance = Math.floor(Math.random() * 20) - 10; // +/- 10%
        return Math.max(5, Math.min(95, plantInfo.value.recommandedHumidityLevel + variance));
    }
    return 60; // Default value
};

const getLastWateredText = () => {
    if (!plant.value || !plant.value.dernier_arrosage) return 'Jamais';
    
    const lastWatering = new Date(plant.value.dernier_arrosage);
    const now = new Date();
    
    const diffMs = now - lastWatering;
    const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
    
    if (diffHrs < 1) return 'À l\'instant';
    if (diffHrs === 1) return 'Il y a 1 heure';
    if (diffHrs < 24) return `Il y a ${diffHrs} heures`;
    
    const diffDays = Math.floor(diffHrs / 24);
    if (diffDays === 1) return 'Il y a 1 jour';
    return `Il y a ${diffDays} jours`;
};

const getLastWateredAmount = () => {
    if (!wateringHistory.value || wateringHistory.value.length === 0) return null;
    
    const lastWatering = wateringHistory.value[0]; // Assuming sorted newest first
    return `${formatTime(lastWatering.date_arrosage)} - ${lastWatering.quantite_eau_ml} ml`;
};

// Load data on mount if a plant is selected
onMounted(() => {
    if (props.selectedPlantId) {
        fetchPlantDetails(props.selectedPlantId);
        fetchWateringHistory(props.selectedPlantId);
    }
});
</script>

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
            <div class="text-info">
                <!-- Basic plant info -->
                <h3>{{ plant.nom }}</h3>
                
                <!-- Stats cards for humidity and last watering -->
                <div class="stats-container">
                    <div class="stat-card">
                        <h4>Humidité actuelle</h4>
                        <div class="stat-value">{{ getHumidityLevel() }}%</div>
                        <div class="stat-chart">
                            <div class="progress-bar">
                                <div class="progress" :style="{ width: getHumidityLevel() + '%' }"></div>
                            </div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <h4>Dernier arrosage</h4>
                        <div class="stat-value">{{ getLastWateredText() }}</div>
                        <div class="last-watered-info" v-if="getLastWateredAmount()">{{ getLastWateredAmount() }}</div>
                    </div>
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
                
                <!-- Watering history section -->
                <div v-if="wateringHistory.length > 0" class="schedule-container">
                    <div class="schedule-header">
                        <h4>Historique d'arrosage</h4>
                        <button class="manual-water-btn" @click="openWateringPopup">
                            Arroser manuellement
                        </button>
                    </div>
                    <ul class="schedule-list">
                        <li class="schedule-item" v-for="(entry, index) in wateringHistory" :key="index">
                            <div class="schedule-time">{{ formatTime(entry.date_arrosage) }}</div>
                            <div class="schedule-action">
                                {{ formatDate(entry.date_arrosage) }} - {{ entry.quantite_eau_ml }} ml
                            </div>
                        </li>
                    </ul>
                </div>
                
                <div class="centrer" v-if="wateringHistory.length === 0">
                    <button class="arrosage-plant-btn" @click="openWateringPopup"> 
                        <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 14 14">
                            <path fill="none" stroke="white" stroke-linecap="round" stroke-linejoin="round" d="M11.5 9C11.5 6.51 7 .5 7 .5S2.5 6.51 2.5 9a4.5 4.5 0 0 0 9 0Z"/>
                        </svg>                    
                        Arrosage
                    </button>
                </div>
            </div>
        </div>
        <div v-else class="no-selection">
            <p>Veuillez sélectionner un semis pour voir les informations détaillées</p>
        </div>
        
        <!-- Watering popup -->
        <div v-if="showWateringPopup" class="popup-overlay">
            <div class="popup-content">
                <div class="popup-header">
                    <h3>Programmer un arrosage</h3>
                    <button class="close-btn" @click="showWateringPopup = false">×</button>
                </div>
                
                <form @submit.prevent="submitWatering" class="watering-form">
                    <div class="form-group">
                        <label for="watering-date">Date:</label>
                        <input 
                            type="date" 
                            id="watering-date" 
                            v-model="wateringForm.date" 
                            required
                        />
                    </div>
                    
                    <div class="form-group">
                        <label for="watering-time">Heure:</label>
                        <input 
                            type="time" 
                            id="watering-time" 
                            v-model="wateringForm.time" 
                            required
                        />
                    </div>
                    
                    <div class="form-group">
                        <label for="watering-duration">Durée (minutes):</label>
                        <input 
                            type="number" 
                            id="watering-duration" 
                            v-model="wateringForm.duration" 
                            required
                            min="1"
                            max="60"
                        />
                    </div>
                    
                    <div class="form-group">
                        <label for="watering-amount">Quantité (ml):</label>
                        <input 
                            type="number" 
                            id="watering-amount" 
                            v-model="wateringForm.amount" 
                            required
                            min="50"
                            max="1000"
                        />
                    </div>
                    
                    <div class="form-actions">
                        <button 
                            type="submit" 
                            class="submit-btn" 
                            :disabled="isSubmitting"
                        >
                            {{ isSubmitting ? 'Enregistrement...' : 'Programmer l\'arrosage' }}
                        </button>
                        <button 
                            type="button" 
                            class="cancel-btn" 
                            @click="showWateringPopup = false"
                            :disabled="isSubmitting"
                        >
                            Annuler
                        </button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Notification toast -->
        <div v-if="showNotification" class="notification" :class="notificationType">
            {{ notificationMessage }}
        </div>
    </div>
</template>

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

.info-title {
    font-weight: bold;
    margin-top: 1rem;
    margin-bottom: 0.2rem;
    color: #95bd75;
}

.info-section {
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

.arrosage-plant-btn {
    margin-top: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    cursor: pointer;
    transition: background-color 0.2s;
    width: 8rem;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
}

.arrosage-plant-btn:hover {
    background-color: #2980b9;
}

.centrer{
    margin-top: 1rem;
    align-items: center;
    justify-items: center;
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

/* Watering schedule styling */
.schedule-container {
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    padding: 1rem;
    margin-top: 1.5rem;
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

.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.popup-content {
    background-color: white;
    border-radius: 0.8rem;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #eee;
}

.popup-header h3 {
    font-family: 'Aeonik-Medium', sans-serif;
    color: #333;
    margin: 0;
}

.close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    color: #888;
    cursor: pointer;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
}

.close-btn:hover {
    background-color: #f5f5f5;
    color: #333;
}

.watering-form {
    padding: 1.5rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    font-weight: 500;
    margin-bottom: 0.5rem;
    color: #333;
}

.form-group input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    font-size: 1rem;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1.5rem;
}

.submit-btn {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 0.5rem;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.submit-btn:hover:not(:disabled) {
    background-color: #2980b9;
}

.cancel-btn {
    background-color: #f5f5f5;
    color: #333;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.cancel-btn:hover:not(:disabled) {
    background-color: #e0e0e0;
}

.submit-btn:disabled,
.cancel-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
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
    
    .schedule-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
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