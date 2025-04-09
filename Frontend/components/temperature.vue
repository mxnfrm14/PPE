<template>
    <div class="stat-card">
        <div class="card-header">
            <h4>{{ title }}</h4>
            <button class="refresh-button" @click="fetchTemperature" :disabled="isLoading"
                title="Rafraîchir les données">
                <span class="refresh-icon" :class="{ 'refreshing': isLoading }">↻</span>
            </button>
        </div>

        <div v-if="isLoading" class="loading">Chargement...</div>

        <template v-else-if="error">
            <div class="error-message">{{ error }}</div>
        </template>

        <template v-else-if="temperatureData">
            <div class="stat-value">{{ temperatureData.temperature }}°C</div>

            <div class="status-info" :class="temperatureData.status">
                <span v-if="temperatureData.status === 'simulated'">(Simulé)</span>
                <span v-else-if="temperatureData.status === 'cached'">(Mise en cache)</span>
            </div>

            <div class="timestamp">
                {{ formatTimestamp(temperatureData.timestamp) }}
            </div>

        </template>

        <template v-else>
            <div class="no-data">Aucune donnée disponible</div>
        </template>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useAuth } from '~/composables/useAuth';

const props = defineProps({
    title: {
        type: String,
        required: true,
    },
    refreshInterval: {
        type: Number,
        default: 3600000, // 1 heure par défaut
    }
});

const { authenticatedFetch } = useAuth();
const temperatureData = ref(null);
const isLoading = ref(false);
const error = ref(null);
let intervalId = null;

// Formater l'horodatage pour une meilleure lisibilité
const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';

    const date = new Date(timestamp.replace(' ', 'T'));
    return new Intl.DateTimeFormat('fr-FR', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    }).format(date);
};

const fetchTemperature = async () => {
    isLoading.value = true;
    error.value = null;

    try {
        const apiBase = useRuntimeConfig().public.apiBaseUrl;
        const response = await authenticatedFetch(`${apiBase}/protected/temperature`);
        console.log('Données de température:', response);

        temperatureData.value = response;
    } catch (err) {
        error.value = err.message || 'Erreur lors de la récupération de la température';
        console.error('Erreur:', err);
    } finally {
        isLoading.value = false;
    }
};

// Configuration de l'actualisation périodique
onMounted(() => {
    // Première récupération
    fetchTemperature();

    // Actualisation périodique
    if (props.refreshInterval > 0) {
        intervalId = setInterval(fetchTemperature, props.refreshInterval);
    }
});

// Nettoyage lors du démontage du composant
onUnmounted(() => {
    if (intervalId) {
        clearInterval(intervalId);
    }
});
</script>

<style scoped>
.stat-card {
    font-family: 'Aeonik-Medium', sans-serif;
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    padding: 1rem;
    flex: 1;
    min-height: 100px;
    position: relative;
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
}

.refresh-icon.refreshing {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.stat-value {
    font-size: 1.8rem;
    font-weight: bold;
    color: #333;
    margin: 0.5rem 0;
}

.timestamp {
    font-size: 0.8rem;
    color: #777;
    margin-bottom: 0.5rem;
}

.status-info {
    font-size: 0.8rem;
    font-style: italic;
    margin-bottom: 0.5rem;
}

.status-info.simulated {
    color: #ff9800;
}

.status-info.cached {
    color: #f44336;
}

.loading {
    color: #666;
    font-size: 1rem;
    margin: 1rem 0;
    font-style: italic;
}

.error-message {
    color: #e74c3c;
    padding: 0.5rem;
    border-radius: 0.4rem;
    background-color: #fdedec;
    margin: 0.5rem 0;
}

.no-data {
    color: #999;
    font-style: italic;
    margin: 1rem 0;
}

h4 {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
    color: #333;
    font: 'Aeonik-Medium';
}
</style>