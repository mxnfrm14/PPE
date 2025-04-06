<template>
    <div v-if="showPopup" class="popup-overlay">
        <div class="popup-content">
            <div class="popup-header">
                <h3>Programmer un arrosage</h3>
                <button class="close-btn" @click="closePopup">×</button>
            </div>
            
            <form @submit.prevent="submitWatering" class="watering-form">
                <div class="form-group">
                    <label for="watering-date">Date:</label>
                    <input 
                        type="date" 
                        id="watering-date" 
                        v-model="formData.date" 
                        required
                    />
                </div>
                
                <div class="form-group">
                    <label for="watering-time">Heure:</label>
                    <input 
                        type="time" 
                        id="watering-time" 
                        v-model="formData.time" 
                        required
                    />
                </div>
                
                <div class="form-group">
                    <label for="watering-duration">Durée (minutes):</label>
                    <input 
                        type="number" 
                        id="watering-duration" 
                        v-model="formData.duration" 
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
                        v-model="formData.amount" 
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
                        @click="closePopup"
                        :disabled="isSubmitting"
                    >
                        Annuler
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useApi } from '~/composables/useApi';

const props = defineProps({
    showPopup: {
        type: Boolean,
        required: true
    },
    plantId: {
        type: String,
        required: true
    }
});

const emit = defineEmits(['close', 'success', 'error']);

const { apiBase, getHeaders, checkAuth } = useApi();
const isSubmitting = ref(false);
const formData = reactive({
    date: new Date().toISOString().split('T')[0],
    time: new Date().toTimeString().slice(0, 5),
    duration: 5,
    amount: 200
});

const closePopup = () => {
    emit('close');
};

const submitWatering = async () => {
    if (!props.plantId) {
        emit('error', 'ID de plante manquant');
        return;
    }
    
    isSubmitting.value = true;
    
    try {
        checkAuth();
        
        // Combine date and time
        const dateTime = `${formData.date}T${formData.time}:00`;
        
        // Prepare data for API
        const wateringData = {
            plantId: props.plantId,
            dateTime: dateTime,
            duration: parseInt(formData.duration),
            amount: parseInt(formData.amount)
        };
        
        // Submit to API
        const response = await $fetch(`${apiBase}/plant/arrosages`, {
            method: 'POST',
            body: wateringData,
            headers: getHeaders()
        });
        
        // Close popup and emit success
        emit('success', {
            message: "Arrosage enregistré avec succès!",
            data: response
        });
        
    } catch (err) {
        console.error('Error submitting watering:', err);
        emit('error', err.message || "Erreur lors de l'ajout de l'arrosage");
    } finally {
        isSubmitting.value = false;
    }
};
</script>

<style scoped>
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
</style>
