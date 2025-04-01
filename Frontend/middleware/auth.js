// middleware/auth.js
export default defineNuxtRouteMiddleware((to, from) => {
  if (process.client) {
    const { isAuthenticated, token } = useAuth();
    
    // Vérifier si le token existe et s'il est valide
    if (!token.value || !isAuthenticated.value) {
      return navigateTo('/login', { 
        query: { redirect: to.fullPath } 
      });
    }
    
    // Vérifier si le token n'est pas expiré
    try {
      // Décodage simple du token (côté client)
      const payload = JSON.parse(atob(token.value.split('.')[1]));
      const expDate = new Date(payload.exp * 1000);
      
      if (expDate < new Date()) {
        // Token expiré
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
        return navigateTo('/login', { 
          query: { redirect: to.fullPath } 
        });
      }
    } catch (e) {
      console.error('Erreur lors de la vérification du token', e);
      return navigateTo('/login');
    }
  }
});