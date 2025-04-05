<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue';
import { useRuntimeConfig } from 'nuxt/app';
import { useAuth } from '~/composables/useAuth';

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

// Load plants when component mounts
onMounted(() => {
    fetchPlants();
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
            <div class="plant-header">{{ findPlantByPosition(position).nom }}</div>
            <div class="plant-info">
              <p>Planté le : {{ formatDate(findPlantByPosition(position).date_plantation) }}</p>
              
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
          <!-- Empty placeholder with plus sign -->
          <div 
            class="plant-card empty-placeholder"
            :style="{ gridArea: `plant-${position}` }"
          >
            <div class="plus-icon">+</div>
          </div>
        </template>
      </template>
    </template>
  </div>
</template>

<style scoped>
.plants-grid {
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
    align-items: center;
    justify-content: center;
    min-height: 120px;
}

.plus-icon {
    font-size: 2rem;
    color: #cccccc;
    font-weight: bold;
}

.loading, .error {
  padding: 2rem;
  text-align: center;
  grid-column: span 3;
}

.error {
  color: #f44336;
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
}
</style>