<script setup lang="ts">
import { NuxtPage } from '#components';
import { onMounted } from 'vue';
import { useAuth } from '~/composables/useAuth';

// Initialize auth on app load but only on client-side
definePageMeta({
  middleware: ['auth']
})
</script>

<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtPage/>
  </div>
</template>