<template>
    <div v-if="show" class="popup-overlay" @click.self="closePopup">
      <div class="popup-content">
        <div class="popup-header">
          <h3>{{ isEditing ? 'Modifier un semis' : 'Ajouter un nouveau semis' }}</h3>
          <button class="close-btn" @click="closePopup">×</button>
        </div>
        
        <form @submit.prevent="submitForm" class="semis-form">
          <div class="form-group">
            <label for="semis-name">Nom du semis*</label>
            <input 
              type="text" 
              id="semis-name" 
              v-model="formData.nom" 
              required
              placeholder="Ex: Tomates, Carottes, Basilic..."
            />
          </div>
          
          <div class="form-group">
            <label for="semis-date">Date de plantation*</label>
            <input 
              type="date" 
              id="semis-date" 
              v-model="formData.date_plantation" 
              required
            />
          </div>
          
          <div class="form-group">
            <label for="semis-watering">Dernier arrosage (optionnel)</label>
            <input 
              type="datetime-local" 
              id="semis-watering" 
              v-model="formData.dernier_arrosage" 
            />
          </div>
          
          <div class="form-group">
            <label for="semis-place">Emplacement</label>
            <input 
              type="number" 
              id="semis-place" 
              v-model="formData.place" 
              disabled
              min="1"
              max="12"
            />
            <small>Position sélectionnée automatiquement</small>
          </div>
          
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
          
          <div class="form-actions">
            <button 
              type="submit" 
              class="submit-btn" 
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? 'Enregistrement...' : (isEditing ? 'Mettre à jour' : 'Ajouter le semis') }}
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
  import { ref, reactive, watch } from 'vue';
  import { useRuntimeConfig } from 'nuxt/app';
  import { useAuth } from '~/composables/useAuth';
  
  // Props
  const props = defineProps({
    show: {
      type: Boolean,
      default: false
    },
    position: {
      type: Number,
      default: null
    },
    existingData: {
      type: Object,
      default: null
    }
  });
  
  // Emits
  const emit = defineEmits(['close', 'submit']);
  
  // Get the API base URL and auth token
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBaseUrl;
  const { token } = useAuth();
  
  // Local state
  const isSubmitting = ref(false);
  const error = ref(null);
  const isEditing = ref(false);
  
  // Form data with defaults
  const formData = reactive({
    nom: '',
    date_plantation: new Date().toISOString().split('T')[0], // Today's date in YYYY-MM-DD format
    dernier_arrosage: '',
    place: props.position || 1,
    _id: null // For editing mode
  });
  
  // Watch for changes in position prop
  watch(() => props.position, (newPosition) => {
    if (newPosition) {
      formData.place = newPosition;
    }
  });
  
  // Watch for existingData to populate form for editing
  watch(() => props.existingData, (data) => {
    if (data) {
      isEditing.value = true;
      
      // Format the dates for the input fields
      const plantedDate = data.date_plantation ? new Date(data.date_plantation).toISOString().split('T')[0] : '';
      
      let lastWatering = '';
      if (data.dernier_arrosage) {
        const date = new Date(data.dernier_arrosage);
        // Format as YYYY-MM-DDThh:mm
        lastWatering = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}T${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
      }
      
      // Populate form data
      formData.nom = data.nom || '';
      formData.date_plantation = plantedDate;
      formData.dernier_arrosage = lastWatering;
      formData.place = data.place || props.position;
      formData._id = data._id || null;
    } else {
      // Reset to adding mode if no existing data
      resetForm();
      isEditing.value = false;
    }
  });
  
  // Function to close the popup
  const closePopup = () => {
    emit('close');
    resetForm();
  };
  
  // Function to reset the form
  const resetForm = () => {
    formData.nom = '';
    formData.date_plantation = new Date().toISOString().split('T')[0];
    formData.dernier_arrosage = '';
    formData.place = props.position || 1;
    formData._id = null;
    error.value = null;
  };
  
  // Function to submit the form
  const submitForm = async () => {
    error.value = null;
    isSubmitting.value = true;
    
    try {
      // Validate required fields
      if (!formData.nom || !formData.date_plantation) {
        throw new Error('Veuillez remplir tous les champs obligatoires');
      }
      
      // Prepare data for API
      const semisData = {
        nom: formData.nom,
        date_plantation: formData.date_plantation,
        place: formData.place
      };
      
      // Add last watering date if provided
      if (formData.dernier_arrosage) {
        semisData.dernier_arrosage = formData.dernier_arrosage;
      }
      
      // Add ID for editing mode
      if (isEditing.value && formData._id) {
        semisData._id = formData._id;
      }
      
      // Call API to create or update
      const endpoint = isEditing.value 
        ? `${apiBase}/plant/semis/${formData._id}`
        : `${apiBase}/plant/semis`;
        
      const method = isEditing.value ? 'PUT' : 'POST';
      
      const response = await $fetch(endpoint, {
        method: method,
        body: semisData,
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      });
      
      // Emit success event with the response data
      emit('submit', response);
      
      // Close popup and reset form
      closePopup();
      
    } catch (err) {
      console.error('Error submitting semis form:', err);
      error.value = err.message || 'Une erreur est survenue lors de l\'enregistrement';
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
  
  .semis-form {
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
  
  .form-group input:focus {
    border-color: #95bd75;
    outline: none;
    box-shadow: 0 0 0 2px rgba(149, 189, 117, 0.2);
  }
  
  .form-group input:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
  }
  
  .form-group small {
    display: block;
    color: #888;
    margin-top: 0.3rem;
    font-size: 0.8rem;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1.5rem;
  }
  
  .submit-btn {
    background-color: #95bd75;
    color: white;
    border: none;
    border-radius: 0.5rem;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .submit-btn:hover:not(:disabled) {
    background-color: #7fa563;
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
  
  .error-message {
    color: #f44336;
    padding: 0.8rem;
    background-color: #ffebee;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
  }
  
  @media (max-width: 640px) {
    .popup-content {
      width: 95%;
    }
    
    .form-actions {
      flex-direction: column;
      gap: 0.5rem;
    }
    
    .submit-btn, .cancel-btn {
      width: 100%;
    }
  }
  </style>