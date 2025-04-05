<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue';
import { useRuntimeConfig } from 'nuxt/app';
import { useAuth } from '~/composables/useAuth';
import SemisForm from '~/components/semis_form.vue';

// Get the API base URL and auth token
const config = useRuntimeConfig();
const apiBase = config.public.apiBaseUrl;
const { token } = useAuth();

// Plants array to hold data from API
const plants = ref([]);
const isLoading = ref(true);
const error = ref(null);

// Selected plant ID with prop for external control
const props = defineProps({
    externalSelectedId: {
        type: String,
        default: null
    }
});

// Watch for external changes to keep local state in sync
const selectedPlantId = ref(props.externalSelectedId);

watch(() => props.externalSelectedId, (newValue) => {
    selectedPlantId.value = newValue;
});

// Emit events to parent
const emit = defineEmits(['plantSelected']);

// Function to handle plant selection
const selectPlant = (plantId) => {
    selectedPlantId.value = plantId;
    emit('plantSelected', plantId);
};

// Function to check if a plant has valid data
const isValidPlant = (plant) => {
    // Check if the plant exists and has necessary data
    return plant && 
           plant.nom && 
           plant.nom.trim() !== '' && 
           plant.date_plantation;
};

// Function to find plant by position
const findPlantByPosition = (position) => {
    return plants.value.find(p => p.place === position);
};

// Function to format ISO date string to readable format
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

// Fetch plants from API
const fetchPlants = async () => {
    isLoading.value = true;
    error.value = null;
    
    try {
        // Check if token exists
        if (!token.value) {
            throw new Error('Vous devez être connecté pour accéder à cette page');
        }
        
        const response = await $fetch(`${apiBase}/plant/semis`, {
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        });
        
        console.log('Fetched plants:', response);
        
        // Sort plants by place (1-12) to ensure they appear in correct order
        plants.value = response.sort((a, b) => a.place - b.place) || [];
    } catch (err) {
        console.error('Error fetching plants:', err);
        error.value = err.message || 'Erreur lors du chargement des semis';
        
        // Redirect to login if unauthorized
        if (err.response?.status === 401) {
            navigateTo('/login');
        }
    } finally {
        isLoading.value = false;
    }
};

// Popup form state
const showSemisForm = ref(false);
const selectedPosition = ref(null);
const selectedPlantForEdit = ref(null);

// Delete confirmation state
const showDeleteConfirm = ref(false);
const plantToDelete = ref(null);
const isDeleting = ref(false);
const deleteError = ref(null);
const deleteSuccess = ref(false);

// Function to open form for adding new semis
const openAddSemisForm = (position) => {
    selectedPosition.value = position;
    selectedPlantForEdit.value = null;
    showSemisForm.value = true;
};

// Function to open form for editing existing semis
const openEditSemisForm = (plant, event) => {
    // Stop the event from propagating to parent (which would select the plant)
    event.stopPropagation();
    
    selectedPosition.value = plant.place;
    selectedPlantForEdit.value = plant;
    showSemisForm.value = true;
};

// Function to show delete confirmation
const confirmDelete = (plant, event) => {
    // Stop the event from propagating to parent
    event.stopPropagation();
    
    plantToDelete.value = plant;
    showDeleteConfirm.value = true;
};

// Function to cancel delete
const cancelDelete = () => {
    plantToDelete.value = null;
    showDeleteConfirm.value = false;
    deleteError.value = null;
};

// Function to handle delete
const deletePlant = async () => {
    if (!plantToDelete.value?._id) return;
    
    isDeleting.value = true;
    deleteError.value = null;
    
    try {
        // Check if token exists
        if (!token.value) {
            throw new Error('Vous devez être connecté pour effectuer cette action');
        }
        
        // Call delete API endpoint
        await $fetch(`${apiBase}/plant/semis/${plantToDelete.value._id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        });
        
        // Show success briefly
        deleteSuccess.value = true;
        
        // Reset selected plant if it was the deleted one
        if (selectedPlantId.value === plantToDelete.value._id) {
            selectedPlantId.value = null;
            emit('plantSelected', null);
        }
        
        // Close confirmation dialog
        showDeleteConfirm.value = false;
        
        // Auto-hide success message after 3 seconds
        setTimeout(() => {
            deleteSuccess.value = false;
        }, 3000);
        
        // Refresh plant list
        await fetchPlants();
    } catch (err) {
        console.error('Error deleting plant:', err);
        deleteError.value = err.message || 'Erreur lors de la suppression du semis';
    } finally {
        isDeleting.value = false;
        plantToDelete.value = null;
    }
};

// Function to handle form submission (add or edit)
const handleSemisFormSubmit = async (data) => {
    console.log('Semis form submitted:', data);
    
    // Refresh plant list
    await fetchPlants();
    
    // Show notification or handle success (you could add a toast notification here)
};

// Load plants when component mounts
onMounted(() => {
    fetchPlants();
});

// Expose methods to parent component
defineExpose({
    fetchPlants
});
</script>


<template>
  <div class="plants-grid">
    <div v-if="isLoading" class="loading">
      Chargement des semis...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <template v-else>
      <!-- Generate all 12 grid positions -->
      <template v-for="position in 12" :key="position">
        <!-- Find if there's a valid plant for this position -->
        <template v-if="findPlantByPosition(position) && isValidPlant(findPlantByPosition(position))">
          <!-- Existing plant card -->
          <div 
            class="plant-card" 
            :class="{ 'active-card': selectedPlantId === findPlantByPosition(position)._id }"
            @click.stop="selectPlant(findPlantByPosition(position)._id)"
            :style="{ gridArea: `plant-${position}` }"
          >
            <div class="plant-header">
              {{ findPlantByPosition(position).nom }}
              <div class="plant-actions">
                <button class="edit-btn" @click.stop="openEditSemisForm(findPlantByPosition(position), $event)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </button>
                <button class="delete-btn" @click.stop="confirmDelete(findPlantByPosition(position), $event)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 6h18"></path>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path>
                    <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    <line x1="10" y1="11" x2="10" y2="17"></line>
                    <line x1="14" y1="11" x2="14" y2="17"></line>
                  </svg>
                </button>
              </div>
            </div>
            <div class="plant-info">
              <p>Planté le : {{ formatDate(findPlantByPosition(position).date_plantation) }}</p>
              <p>Arrosé le : {{ formatDate(findPlantByPosition(position).dernier_arrosage) }}</p>
              
              <button class="afficher-plant-btn" @click.stop="selectPlant(findPlantByPosition(position)._id)">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 14 14">
                  <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M7 13.5a6.5 6.5 0 1 0 0-13a6.5 6.5 0 0 0 0 13M7 4v6M4 7h6"></path>
                </svg>                        
                Afficher plus
              </button>
            </div>
          </div>
        </template>
        <template v-else>
          <!-- Empty placeholder with plus sign - Clickable -->
          <div 
            class="plant-card empty-placeholder"
            :style="{ gridArea: `plant-${position}` }"
            @click="openAddSemisForm(position)"
          >
            <div class="plus-icon">+</div>
            <div class="placeholder-text">Ajouter un semis</div>
          </div>
        </template>
      </template>
    </template>
    
    <!-- Semis Form Component -->
    <SemisForm
      :show="showSemisForm"
      :position="selectedPosition"
      :existingData="selectedPlantForEdit"
      @close="showSemisForm = false"
      @submit="handleSemisFormSubmit"
    />
    
    <!-- Delete Confirmation Dialog -->
    <div v-if="showDeleteConfirm" class="confirmation-overlay">
      <div class="confirmation-dialog">
        <div class="confirmation-header">
          <h3>Confirmer la suppression</h3>
        </div>
        <div class="confirmation-content">
          <p>Êtes-vous sûr de vouloir supprimer <strong>{{ plantToDelete ? plantToDelete.nom : '' }}</strong> ?</p>
          <p class="warning">Cette action est irréversible et supprimera également l'historique d'arrosage associé.</p>
          
          <div v-if="deleteError" class="delete-error">
            {{ deleteError }}
          </div>
        </div>
        <div class="confirmation-actions">
          <button 
            @click="deletePlant" 
            class="confirm-delete-btn" 
            :disabled="isDeleting"
          >
            {{ isDeleting ? 'Suppression...' : 'Supprimer' }}
          </button>
          <button 
            @click="cancelDelete" 
            class="cancel-btn" 
            :disabled="isDeleting"
          >
            Annuler
          </button>
        </div>
      </div>
    </div>
    
    <!-- Success Notification -->
    <div v-if="deleteSuccess" class="success-notification">
      Semis supprimé avec succès
    </div>
  </div>
</template>

<style scoped>
.plants-grid {
    font-family: 'Aeonik-Medium', sans-serif;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(4, auto);
    grid-template-areas: 
      "plant-1 plant-2 plant-3"
      "plant-4 plant-5 plant-6"
      "plant-7 plant-8 plant-9"
      "plant-10 plant-11 plant-12";
    gap: 0.05rem;
    margin-bottom: 1.5rem;
    border-radius: 0.8rem;
    position: relative; /* For absolute positioned notifications */
}

.plant-card {
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    overflow: hidden;
    margin: 0.6rem;
    box-shadow: 1px 3px 3px 1px #d8d8d8;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    border: 2px solid transparent;
}

.plant-header {
    background-color: #95bd75;
    color: white;
    font-weight: bold;
    padding: 0.8rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.plant-actions {
    display: flex;
    gap: 0.5rem;
}

.edit-btn, .delete-btn {
    background: none;
    border: none;
    color: white;
    padding: 0.2rem;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.7;
    transition: opacity 0.2s, background-color 0.2s;
}

.edit-btn:hover {
    opacity: 1;
    background-color: rgba(255, 255, 255, 0.2);
}

.delete-btn {
    color: #ffcccc;
}

.delete-btn:hover {
    opacity: 1;
    background-color: rgba(255, 0, 0, 0.2);
}

.plant-info {
    padding: 1rem;
}

.plant-info p {
    margin: 0.3rem 0;
    color: #444;
}

.afficher-plant-btn {
    margin-top: 1rem;
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 0.4rem;
    padding: 0.5rem 0.8rem;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.3rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.afficher-plant-btn:hover {
    background-color: #e4e4e4;
}

.active-card {
    border: 5px solid #95bd75;
    box-shadow: 0 0 8px rgba(149, 189, 117, 0.6);
    transform: translateY(-2px);
}

.empty-placeholder {
    background-color: transparent;
    border: 2px dashed #cccccc;
    box-shadow: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 120px;
    transition: background-color 0.2s, border-color 0.2s;
}

.empty-placeholder:hover {
    background-color: #f9f9f9;
    border-color: #95bd75;
}

.plus-icon {
    font-size: 2rem;
    color: #cccccc;
    font-weight: bold;
    transition: color 0.2s;
}

.empty-placeholder:hover .plus-icon {
    color: #95bd75;
}

.placeholder-text {
    margin-top: 0.5rem;
    font-size: 0.8rem;
    color: #888;
    transition: color 0.2s;
}

.empty-placeholder:hover .placeholder-text {
    color: #95bd75;
}

.loading, .error {
  padding: 2rem;
  text-align: center;
  grid-column: span 3;
}

.error {
  color: #f44336;
}

/* Delete confirmation dialog */
.confirmation-overlay {
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

.confirmation-dialog {
    background-color: white;
    border-radius: 0.8rem;
    width: 90%;
    max-width: 400px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    overflow: hidden;
}

.confirmation-header {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #eee;
}

.confirmation-header h3 {
    margin: 0;
    color: #333;
    font-family: 'Aeonik-Medium', sans-serif;
}

.confirmation-content {
    padding: 1.5rem;
}

.confirmation-content p {
    margin: 0.5rem 0;
    color: #333;
}

.warning {
    color: #f44336;
    font-size: 0.9rem;
    margin-top: 1rem;
}

.delete-error {
    background-color: #ffebee;
    color: #f44336;
    padding: 0.75rem;
    border-radius: 0.5rem;
    margin-top: 1rem;
    font-size: 0.9rem;
}

.confirmation-actions {
    display: flex;
    justify-content: flex-end;
    padding: 1rem 1.5rem;
    border-top: 1px solid #eee;
    gap: 1rem;
}

.confirm-delete-btn {
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 0.5rem;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.confirm-delete-btn:hover:not(:disabled) {
    background-color: #e53935;
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

.confirm-delete-btn:disabled,
.cancel-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* Success notification */
.success-notification {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #4caf50;
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    z-index: 1001;
    animation: fadeIn 0.3s, fadeOut 0.3s 2.7s;
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
    .plants-grid {
        grid-template-columns: 1fr;
        grid-template-areas: 
          "plant-1" "plant-2" "plant-3"
          "plant-4" "plant-5" "plant-6"
          "plant-7" "plant-8" "plant-9"
          "plant-10" "plant-11" "plant-12";
    }
    
    .confirmation-actions {
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .confirm-delete-btn, .cancel-btn {
        width: 100%;
    }
}
</style>