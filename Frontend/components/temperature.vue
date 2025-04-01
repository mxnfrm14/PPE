<template>
    <div class="stat-card">
        <h4>{{ title }}</h4>
        
        <div v-if="isLoading" class="loading">Chargement...</div>
        
        <template v-else-if="error">
            <div class="error-message">{{ error }}</div>
        </template>
        
        <template v-else-if="temperature !== null">
            <div class="stat-value">{{ temperature }}°C</div>
            <div class="temp-range">
                <span>Min: 18°C</span>
                <span>Max: 28°C</span> 
                <!-- on peut mettre la derniere date enregistrer -->
            </div>
        </template>
        
        <template v-else>
            <div class="no-data">Aucune donnée disponible</div>
        </template>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuth } from '~/composables/useAuth';

const props = defineProps({
    title: {
        type: String,
        required: true,
    },
});

const { authenticatedFetch } = useAuth();
const temperature = ref(null);
const isLoading = ref(false);
const error = ref(null);

const fetchTemperature = async () => {
    isLoading.value = true;
    error.value = null;
    
    try {
        // Notez le préfixe /api ici
        const response = await authenticatedFetch('/api/protected/temperature');
        console.log('Données de température:', response);
        
        if (response && 'temperature' in response) {
            temperature.value = response.temperature;
        } else {
            error.value = 'Format de réponse incorrect';
        }
    } catch (err) {
        error.value = err.message || 'Erreur lors de la récupération de la température';
        console.error('Erreur:', err);
    } finally {
        isLoading.value = false;
    }
};
// Appeler la fonction au montage du composant
onMounted(fetchTemperature);
</script>

<style scoped>
.stat-card {
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    padding: 1rem;
    flex: 1;
    min-height: 150px;
}

.stat-value {
    font-size: 1.8rem;
    font-weight: bold;
    color: #333;
    margin: 0.5rem 0;
}

.temp-range {
    display: flex;
    justify-content: space-between;
    color: #666;
    font-size: 0.9rem;
    margin-top: 0.5rem;
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
</style>