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
import { ref, onMounted, onUnmounted } from 'vue';
import { useAuth } from '~/composables/useAuth';
import { useRouter } from 'vue-router';

const router = useRouter();
const { user, logout } = useAuth();
const contentSemisRef = ref(null);
const semisContainerRef = ref(null);

// Add a ref to track the selected plant
const selectedPlantId = ref(null);

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

// Add and remove event listeners
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
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
      <header_title
        title="Gestion des Semis"
        subtitle="Contrôle et suivi"
        class="header_title"
      ></header_title>
    </div>
    <div class="content">
      <div class="main">

        <div class="container-temperatures">
          <indicators
            iconBackgroundColor="#95BD75"
            iconPath="/assets/images/thermometer.png"
            subtitle=" "
            title="Température serre :"
          />
          <indicators
            iconBackgroundColor="#d8d8d8"
            iconPath="/assets/images/thermometer.png"
            subtitle=" "
            title="Température système :"
          />
        </div>

        <div class="container-etagere-info" ref="semisContainerRef">
          <blocSemis 
            @plant-selected="handlePlantSelected" 
            :external-selected-id="selectedPlantId" 
          />
          <blocInfos :selected-plant-id="selectedPlantId" />
        </div>
        

        <div class="redirect">
          <button
            type="button"
            class="Arrosage"
            @click="changeView('arrosage')"
          >
            <indicators
              iconBackgroundColor="#95BD75"
              iconPath="/assets/images/watering-can-plant.png"
              subtitle=" "
              title="Arrosage des semis"
            />
          </button>
          <button
            type="button"
            class="Température"
            @click="changeView('temperature')"
          >
          <indicators
            iconBackgroundColor="#95BD75"
            iconPath="/assets/images/thermometer.png"
            subtitle=" "
            title="Température"
          /></button>

          <button
            type="button"
            class="plantations"
            @click="changeView('plantations')"
          >
          <indicators
            iconBackgroundColor="#95BD75"
            iconPath="/assets/images/potted-plant.png"
            subtitle=" "
            title="Gérer les plantations"
          /></button>
        </div>

        <div class="content-section">
          <ContentSemis ref="contentSemisRef" />
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.container-temperatures {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
}

.container-etagere-info {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}

.wrapper_page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
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

.swich-mode {
  margin-top: 1.5rem;
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
  .redirect {
    flex-direction: column;
    align-items: center;
  }
}
</style>