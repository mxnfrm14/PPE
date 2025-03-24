<template>
    <div class="led-control">
        <div class="toggle-switch" @click="toggleLED">
            <div class="toggle-track" :class="{ 'active': isLEDOn }">
                <div class="toggle-indicator" :class="{ 'active': isLEDOn }"></div>
            </div>
            <span class="toggle-label">{{ isLEDOn ? 'LED Allumée' : 'LED Éteinte' }}</span>
        </div>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="statusMessage" class="status-message">{{ statusMessage }}</div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const isLEDOn = ref(false);
const errorMessage = ref('');
const statusMessage = ref('');

const toggleLED = async () => {
    errorMessage.value = '';
    statusMessage.value = '';
    
    try {
        // Inverser l'état actuel
        const newState = !isLEDOn.value;
        
        // Appeler l'API pour changer l'état de la LED
        const response = await $fetch("/api/led/toggle", {
            method: 'POST',
            body: {
                state: newState ? "on" : "off"
            }
        });
        
        if (response.status === "success") {
            isLEDOn.value = newState;
            statusMessage.value = response.message;
        } else {
            errorMessage.value = "Erreur lors du changement d'état de la LED";
        }
    } catch (err) {
        console.error("Erreur lors de la communication avec l'API:", err);
        errorMessage.value = err.message || "Erreur de communication avec le serveur";
    }
};
</script>

<style scoped>
.led-control {
    margin: 1rem 0;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.toggle-switch {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
}

.toggle-track {
    position: relative;
    width: 3.5rem;
    height: 1.5rem;
    background-color: #cccccc;
    border-radius: 1rem;
    transition: background-color 0.3s ease;
}

.toggle-track.active {
    background-color: #ff5722; /* Couleur orange/rouge pour représenter la LED allumée */
}

.toggle-indicator {
    position: absolute;
    top: 0.15rem;
    left: 0.15rem;
    width: 1.2rem;
    height: 1.2rem;
    background-color: white;
    border-radius: 50%;
    transition: transform 0.3s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.toggle-indicator.active {
    transform: translateX(2rem);
}

.toggle-label {
    margin-top: 0.3rem;
    font-size: 0.8rem;
    font-family: 'Aeonik-Regular';
    color: #333;
}

.error-message {
    color: red;
    margin-top: 0.5rem;
    font-size: 0.8rem;
}

.status-message {
    color: green;
    margin-top: 0.5rem;
    font-size: 0.8rem;
}
</style>