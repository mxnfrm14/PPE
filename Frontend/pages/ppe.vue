<script setup lang="ts">
// Apply auth middleware to protect this page
definePageMeta({
  middleware: ['auth']
});

import Header_title from "~/components/header_title.vue";
import indicators from "~/components/indicators.vue";
import swichMode from "~/components/switch_mode.vue";
import ContentSemis from "~/components/content_semis.vue";
import navbar from "~/components/navbar.vue";
import { ref } from 'vue';
import { useAuth } from '~/composables/useAuth';
import { useRouter } from 'vue-router';

const router = useRouter();
const { user, logout } = useAuth();
const contentSemisRef = ref(null);

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
        <div class="swich-mode">
          <swichMode title="Mode de gestion automatique" subtitle="Contrôle de l'arrosage" />
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