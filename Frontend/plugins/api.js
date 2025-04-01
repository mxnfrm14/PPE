// plugins/api.js
export default defineNuxtPlugin(nuxtApp => {
    const { token, isAuthenticated } = useAuth();
    
    // Étendre $fetch avec une version authentifiée
    nuxtApp.provide('authFetch', async (url, options = {}) => {
      if (!token.value) {
        console.warn('Tentative de requête authentifiée sans token');
        
        // Si vous voulez bloquer la requête
        if (options.requireAuth !== false) {
          throw new Error('Authentication requise');
        }
        
        // Sinon continuer sans token
        return $fetch(url, options);
      }
      
      const headers = {
        ...(options.headers || {}),
        Authorization: `Bearer ${token.value}`
      };
      
      try {
        return await $fetch(url, {
          ...options,
          headers
        });
      } catch (error) {
        if (error.response?.status === 401) {
          isAuthenticated.value = false;
          // Gérer l'expiration du token
          navigateTo('/login');
        }
        throw error;
      }
    });
  });