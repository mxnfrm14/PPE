<script setup lang="ts">
// Apply auth middleware to protect this page
definePageMeta({
  middleware: ['auth']
});

import Header_title from "~/components/header_title.vue";
import indicators from "~/components/indicators.vue";
import ContentSemis from "~/components/content_semis.vue";
import navbar from "~/components/navbar.vue";
import blocSemis from "~/components/bloc_semis.vue";
import blocInfos from "~/components/infos_semis.vue";
import SemisForm from "~/components/semis_form.vue";
import temperature from "~/components/temperature.vue";
import { ref, onMounted, onUnmounted } from 'vue';
import { useAuth } from '~/composables/useAuth';
import { useRouter } from 'vue-router';
import { useRuntimeConfig } from 'nuxt/app';

const router = useRouter();
const { user, logout } = useAuth();
const contentSemisRef = ref(null);
const semisContainerRef = ref(null);
const blocSemisRef = ref(null);

// Add a ref to track if refreshing
const isRefreshing = ref(false);

// Add a ref to track the selected plant
const selectedPlantId = ref(null);

// Add refs for form component
const showSemisForm = ref(false);
const selectedPosition = ref(null);
const selectedPlantForEdit = ref(null);

// Add refs for delete confirmation
const showDeleteConfirm = ref(false);
const plantToDelete = ref(null);
const isDeleting = ref(false);
const deleteError = ref(null);
const deleteSuccess = ref(false);

// Get the API base URL and auth token
const config = useRuntimeConfig();
const apiBase = config.public.apiBaseUrl;
const { token } = useAuth();

// Function to refresh plant data
const refreshPlants = async () => {
  isRefreshing.value = true;
  
  try {
    // Check if the blocSemisRef exists and has a fetchPlants method
    if (blocSemisRef.value && typeof blocSemisRef.value.fetchPlants === 'function') {
      await blocSemisRef.value.fetchPlants();
      console.log('Plants refreshed successfully');
    }
    
    // If we have a selected plant ID, refresh that plant's details
    if (selectedPlantId.value) {
      // Re-fetch the selected plant details if needed
      const response = await $fetch(`${apiBase}/plant/semis/${selectedPlantId.value}`, {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      });
      
      // Check if the plant still exists, if not, clear selection
      if (!response) {
        selectedPlantId.value = null;
      }
    }
  } catch (err) {
    console.error('Error refreshing plants:', err);
    // If the selected plant was deleted, clear selection
    if (err.response?.status === 404 && selectedPlantId.value) {
      selectedPlantId.value = null;
    }
  } finally {
    isRefreshing.value = false;
  }
};

// Handle plant selection from blocSemis
const handlePlantSelected = (plantId) => {
  selectedPlantId.value = plantId;
};

// Handle click outside of the semis container
const handleClickOutside = (event) => {
  // Check if the semis container exists and if the click is outside of it
  if (semisContainerRef.value && !semisContainerRef.value.contains(event.target)) {
    // Reset the selected plant
    selectedPlantId.value = null;
  }
};

// Handle edit request from either component
const handleEditPlant = (plant) => {
  selectedPlantForEdit.value = plant;
  selectedPosition.value = plant.place;
  showSemisForm.value = true;
};

// Handle delete confirmation request from either component
const handleDeleteRequest = (plant) => {
  plantToDelete.value = plant;
  showDeleteConfirm.value = true;
};

// Function to cancel delete
const cancelDelete = () => {
  plantToDelete.value = null;
  showDeleteConfirm.value = false;
  deleteError.value = null;
};

// Function to perform deletion
const deletePlant = async () => {
  if (!plantToDelete.value?._id) return;
  
  isDeleting.value = true;
  deleteError.value = null;
  
  try {
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
    }
    
    // Close confirmation dialog
    showDeleteConfirm.value = false;
    
    // Auto-hide success message after 3 seconds
    setTimeout(() => {
      deleteSuccess.value = false;
    }, 3000);
    
    // Refresh the plants list
    await refreshPlants();
    
  } catch (err) {
    console.error('Error deleting plant:', err);
    deleteError.value = err.message || 'Erreur lors de la suppression du semis';
  } finally {
    isDeleting.value = false;
  }
};

// Handle semis form submission
const handleSemisFormSubmit = async (data) => {
  // Form was submitted successfully
  console.log('Semis form submitted:', data);
  
  // Reset the form
  showSemisForm.value = false;
  selectedPlantForEdit.value = null;
  
  // Refresh the plants list
  await refreshPlants();
};

// Add and remove event listeners
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  
  // Initial refresh
  refreshPlants();
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

const changeView = (view) => {
  if (contentSemisRef.value) {
    contentSemisRef.value.setView(view);
  }
};

const handleLogout = () => {
  logout();
  router.push('/login');
};
</script>

<template>
  <div class="wrapper_page">
    <navbar></navbar>
    <div class="header_bis">
      <header_title title="Gestion des Semis" subtitle="Contrôle et suivi" class="header_title"></header_title>
    </div>
    <div class="content">
      <div class="main">

        <div class="container-temperatures">
          <temperature title="Température serre" />
          <temperature title="Température composants" />
        </div>
        
        <!-- Title with refresh button for semis section -->
        <div class="section-header">
          <h2>Vue d'ensemble des semis</h2>
          <button @click="refreshPlants" class="refresh-btn" :class="{ 'refreshing': isRefreshing }" :disabled="isRefreshing">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M23 4v6h-6"></path>
              <path d="M1 20v-6h6"></path>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
            </svg>
            <span>{{ isRefreshing ? 'Actualisation...' : 'Actualiser' }}</span>
          </button>
        </div>

        <div class="container-etagere-info" ref="semisContainerRef">
          <blocSemis 
            ref="blocSemisRef"
            @plant-selected="handlePlantSelected" 
            :external-selected-id="selectedPlantId" 
          />
          <blocInfos 
            :selected-plant-id="selectedPlantId" 
            @edit-plant="handleEditPlant"
            @delete-plant="handleDeleteRequest"
          />
        </div>
      </div>


    </div>
    
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
.container-temperatures {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e0e0e0;
}

.section-header h2 {
  font-family: 'Aeonik-Bold', sans-serif;
  font-size: 1.5rem;
  color: #333;
  margin: 0;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  color: #333;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background-color: #e0e0e0;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-btn svg {
  transition: transform 0.5s ease;
}

.refresh-btn.refreshing svg {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.container-etagere-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.wrapper_page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
}

.header_bis {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  margin: 1rem;
}

.main {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 1rem;
  padding: 1rem;
  flex: 1;
}

.redirect {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1.5rem;
}

.content {
  display: flex;
  flex-direction: row;
  flex: 1;
}

.content-section {
  margin-top: 1rem;
}

.side-calendar {
  display: flex;
  justify-content: center;
  align-items: start;
  flex: 0 0 500px;
  padding: 1rem;
}

button {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  transition: transform 0.2s;
}

button:hover {
  transform: translateY(-2px);
}

.redirect button:hover {
  transform: translateY(-2px);
}

.swich-mode {
  margin-top: 1.5rem;
}

/* Confirmation dialog styles */
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

@media (max-width: 992px) {
  .content {
    flex-direction: column;
  }

  .side-calendar {
    flex: 1;
    width: 100%;
    margin-top: 1rem;
  }
}

@media (max-width: 768px) {
  .container-etagere-info {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .refresh-btn {
    align-self: flex-end;
  }
  
  .redirect {
    flex-direction: column;
    align-items: center;
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